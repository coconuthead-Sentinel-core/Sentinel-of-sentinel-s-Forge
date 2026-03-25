"""Tests for JWT authentication system."""
import pytest
from unittest.mock import patch
from fastapi import HTTPException

from backend.core.auth import (
    UserCreate,
    create_user,
    authenticate_user,
    create_token_pair,
    decode_token,
    get_user_by_id,
    update_user_subscription,
)
from backend.infrastructure.user_repository import user_repository


@pytest.fixture(autouse=True)
def clean_users():
    """Clear user store between tests."""
    user_repository.clear_local_cache()
    yield
    user_repository.clear_local_cache()


def test_create_user():
    """Users can be created with hashed passwords."""
    data = UserCreate(email="test@example.com", password="securepass123", display_name="Tester")
    user = create_user(data)
    assert user.email == "test@example.com"
    assert user.display_name == "Tester"
    assert user.hashed_password != "securepass123"  # Must be hashed
    stored = get_user_by_id(user.id)
    assert stored is not None
    assert stored.email == "test@example.com"


def test_create_duplicate_email_fails():
    """Duplicate email registration should fail."""
    data = UserCreate(email="dupe@example.com", password="securepass123")
    create_user(data)
    with pytest.raises(HTTPException) as exc:
        create_user(data)
    assert exc.value.status_code == 409


def test_authenticate_user_success():
    """Valid credentials return the user."""
    data = UserCreate(email="auth@example.com", password="mypassword99")
    create_user(data)
    user = authenticate_user("auth@example.com", "mypassword99")
    assert user is not None
    assert user.email == "auth@example.com"


def test_authenticate_user_wrong_password():
    """Wrong password returns None."""
    data = UserCreate(email="auth2@example.com", password="correctpass")
    create_user(data)
    assert authenticate_user("auth2@example.com", "wrongpass") is None


def test_authenticate_user_unknown_email():
    """Unknown email returns None."""
    assert authenticate_user("nobody@example.com", "whatever") is None


def test_token_creation_and_decoding():
    """Tokens can be created and decoded."""
    with patch("backend.core.auth.settings") as mock_settings:
        mock_settings.JWT_SECRET_KEY = "test-secret-key-for-testing"
        mock_settings.JWT_ALGORITHM = "HS256"
        mock_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
        mock_settings.is_production = False

        data = UserCreate(email="token@example.com", password="tokenpass123")
        user = create_user(data)
        tokens = create_token_pair(user)

        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type == "bearer"
        assert tokens.expires_in == 1800  # 30 min * 60 sec

        # Decode access token
        payload = decode_token(tokens.access_token)
        assert payload["sub"] == user.id
        assert payload["email"] == "token@example.com"
        assert payload["type"] == "access"

        # Decode refresh token
        payload = decode_token(tokens.refresh_token)
        assert payload["sub"] == user.id
        assert payload["type"] == "refresh"


def test_email_case_insensitive():
    """Email matching is case-insensitive."""
    data = UserCreate(email="Mixed@CASE.com", password="password123")
    create_user(data)
    user = authenticate_user("mixed@case.com", "password123")
    assert user is not None


def test_get_user_by_id():
    """Users can be looked up by ID."""
    data = UserCreate(email="lookup@example.com", password="password123")
    user = create_user(data)
    found = get_user_by_id(user.id)
    assert found is not None
    assert found.email == "lookup@example.com"
    assert get_user_by_id("nonexistent-id") is None


def test_update_user_subscription_persists():
    """Subscription updates should persist through repository storage."""
    data = UserCreate(email="billing@example.com", password="password123")
    user = create_user(data)
    update_user_subscription(user.id, "pro", "cus_123")

    stored = get_user_by_id(user.id)
    assert stored is not None
    assert stored.subscription_tier == "pro"
    assert stored.stripe_customer_id == "cus_123"
