"""HTTP-level integration tests for auth, billing, and health routes.

Uses FastAPI TestClient to exercise the full request/response cycle.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from backend.infrastructure.user_repository import user_repository


@pytest.fixture(autouse=True)
def clean_users():
    """Clear user store between tests."""
    user_repository.clear_local_cache()
    yield
    user_repository.clear_local_cache()


@pytest.fixture()
def client():
    """Create a TestClient for the FastAPI app."""
    # Patch out lifespan tasks that require external services
    mock_cosmos = MagicMock()
    mock_cosmos.initialize = AsyncMock(return_value=None)
    mock_cosmos.close = AsyncMock(return_value=None)

    mock_provider = MagicMock()
    mock_provider.get_token = AsyncMock(return_value="mock-token")
    mock_provider.aclose = AsyncMock(return_value=None)

    with patch("backend.main.CosmosDBRepository", mock_cosmos), \
         patch("backend.main.AzureCognitiveTokenProvider", return_value=mock_provider):
        from backend.main import app
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c


# ------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------

class TestHealthz:
    def test_healthz_returns_ok(self, client: TestClient):
        resp = client.get("/api/healthz")
        assert resp.status_code in (200, 204)


# ------------------------------------------------------------------
# Auth flow: signup → login → profile → refresh
# ------------------------------------------------------------------

class TestAuthFlow:
    def test_signup_returns_tokens(self, client: TestClient):
        resp = client.post("/api/auth/signup", json={
            "email": "new@example.com",
            "password": "securepass123",
            "display_name": "New User",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_signup_duplicate_email_409(self, client: TestClient):
        payload = {
            "email": "dup@example.com",
            "password": "securepass123",
            "display_name": "Dup",
        }
        client.post("/api/auth/signup", json=payload)
        resp = client.post("/api/auth/signup", json=payload)
        assert resp.status_code == 409

    def test_login_returns_tokens(self, client: TestClient):
        client.post("/api/auth/signup", json={
            "email": "login@example.com",
            "password": "securepass123",
        })
        resp = client.post("/api/auth/login", json={
            "email": "login@example.com",
            "password": "securepass123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data

    def test_login_wrong_password_401(self, client: TestClient):
        client.post("/api/auth/signup", json={
            "email": "wrong@example.com",
            "password": "securepass123",
        })
        resp = client.post("/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "badpassword",
        })
        assert resp.status_code == 401

    def test_profile_with_valid_token(self, client: TestClient):
        signup = client.post("/api/auth/signup", json={
            "email": "me@example.com",
            "password": "securepass123",
            "display_name": "Me",
        })
        token = signup.json()["access_token"]
        resp = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        profile = resp.json()
        assert profile["email"] == "me@example.com"
        assert profile["display_name"] == "Me"
        assert profile["subscription_tier"] == "free"

    def test_profile_without_token_returns_mock_in_dev(self, client: TestClient):
        # In dev mode, missing auth returns mock user
        resp = client.get("/api/auth/me")
        assert resp.status_code == 200
        profile = resp.json()
        assert profile["email"] == "dev@localhost"

    def test_refresh_returns_new_tokens(self, client: TestClient):
        signup = client.post("/api/auth/signup", json={
            "email": "refresh@example.com",
            "password": "securepass123",
        })
        refresh_token = signup.json()["refresh_token"]
        resp = client.post("/api/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data


# ------------------------------------------------------------------
# Billing flow: list plans → subscription status → checkout
# ------------------------------------------------------------------

class TestBillingFlow:
    def _signup_and_get_token(self, client: TestClient, email: str = "bill@example.com") -> str:
        resp = client.post("/api/auth/signup", json={
            "email": email,
            "password": "securepass123",
        })
        return resp.json()["access_token"]

    def test_list_plans_returns_three_tiers(self, client: TestClient):
        resp = client.get("/api/billing/plans")
        assert resp.status_code == 200
        data = resp.json()
        assert "plans" in data
        plan_ids = {p["id"] for p in data["plans"]}
        assert plan_ids == {"starter", "pro", "enterprise"}

    def test_subscription_status_default_free(self, client: TestClient):
        token = self._signup_and_get_token(client)
        resp = client.get("/api/billing/subscription", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["tier"] == "free"

    def test_checkout_returns_url(self, client: TestClient):
        token = self._signup_and_get_token(client, "checkout@example.com")
        resp = client.post("/api/billing/checkout", json={
            "plan": "starter",
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
        }, headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "checkout_url" in data
        assert "session_id" in data
