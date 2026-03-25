"""Tests for startup security configuration validation."""
from unittest.mock import patch

import pytest

from backend.core.config import validate_security_configuration


def test_validate_security_configuration_allows_non_production():
    with patch("backend.core.config.settings") as mock_settings:
        mock_settings.is_production = False
        mock_settings.API_KEY = ""
        mock_settings.JWT_SECRET_KEY = ""
        validate_security_configuration()


def test_validate_security_configuration_rejects_missing_jwt_secret():
    with patch("backend.core.config.settings") as mock_settings:
        mock_settings.is_production = True
        mock_settings.API_KEY = "api-key"
        mock_settings.JWT_SECRET_KEY = ""

        with pytest.raises(RuntimeError) as exc:
            validate_security_configuration()

        assert "JWT_SECRET_KEY" in str(exc.value)


def test_validate_security_configuration_accepts_required_production_secrets():
    with patch("backend.core.config.settings") as mock_settings:
        mock_settings.is_production = True
        mock_settings.API_KEY = "api-key"
        mock_settings.JWT_SECRET_KEY = "a" * 64  # Strong 64-char secret
        validate_security_configuration()


def test_validate_security_configuration_rejects_weak_jwt_secret():
    with patch("backend.core.config.settings") as mock_settings:
        mock_settings.is_production = True
        mock_settings.API_KEY = "api-key"
        mock_settings.JWT_SECRET_KEY = "changeme"

        with pytest.raises(RuntimeError) as exc:
            validate_security_configuration()

        assert "weak" in str(exc.value).lower()


def test_validate_security_configuration_rejects_short_jwt_secret():
    with patch("backend.core.config.settings") as mock_settings:
        mock_settings.is_production = True
        mock_settings.API_KEY = "api-key"
        mock_settings.JWT_SECRET_KEY = "short-secret"

        with pytest.raises(RuntimeError) as exc:
            validate_security_configuration()

        assert "32 characters" in str(exc.value)
