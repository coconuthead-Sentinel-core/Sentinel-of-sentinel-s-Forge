"""Tests for Stripe billing configuration behavior."""
import asyncio
from types import SimpleNamespace

import pytest

from backend.core.auth import UserRecord
from backend.routes import billing_routes


@pytest.fixture(autouse=True)
def reset_stripe_cache():
    """Reset the module-level Stripe cache between tests."""
    original = billing_routes._stripe
    billing_routes._stripe = None
    yield
    billing_routes._stripe = original


def test_get_price_id_returns_configured_plan(monkeypatch):
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_STARTER", "price_starter")
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_PRO", "price_pro")
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_ENTERPRISE", "price_enterprise")

    assert billing_routes._get_price_id("starter") == "price_starter"
    assert billing_routes._get_price_id("pro") == "price_pro"
    assert billing_routes._get_price_id("enterprise") == "price_enterprise"


def test_create_checkout_returns_mock_response_without_stripe_secret(monkeypatch):
    monkeypatch.setattr(billing_routes.settings, "STRIPE_SECRET_KEY", "")
    monkeypatch.setattr(billing_routes, "_stripe", object())

    response = asyncio.run(
        billing_routes.create_checkout(
            billing_routes.CreateCheckoutRequest(plan="starter"),
            UserRecord("user-12345678", "billing@example.com", "hashed"),
        )
    )

    assert response.checkout_url == "https://checkout.stripe.com/mock?plan=starter"
    assert response.session_id == "mock_session_user-123"


def test_create_checkout_uses_stripe_session_when_runtime_configured(monkeypatch):
    calls: dict[str, object] = {}

    def fake_create(**kwargs):
        calls.update(kwargs)
        return SimpleNamespace(url="https://checkout.stripe.com/pay/cs_test_123", id="cs_test_123")

    fake_stripe = SimpleNamespace(
        checkout=SimpleNamespace(
            Session=SimpleNamespace(create=fake_create)
        )
    )

    monkeypatch.setattr(billing_routes.settings, "STRIPE_SECRET_KEY", "sk_test_123")
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_STARTER", "price_starter")
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_PRO", "price_pro")
    monkeypatch.setattr(billing_routes.settings, "STRIPE_PRICE_ID_ENTERPRISE", "price_enterprise")
    monkeypatch.setattr(billing_routes, "_stripe", fake_stripe)

    response = asyncio.run(
        billing_routes.create_checkout(
            billing_routes.CreateCheckoutRequest(
                plan="starter",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
            ),
            UserRecord("user-12345678", "billing@example.com", "hashed"),
        )
    )

    assert response.checkout_url == "https://checkout.stripe.com/pay/cs_test_123"
    assert response.session_id == "cs_test_123"
    assert calls["mode"] == "subscription"
    assert calls["line_items"] == [{"price": "price_starter", "quantity": 1}]
    assert calls["metadata"] == {"user_id": "user-12345678", "plan": "starter"}
