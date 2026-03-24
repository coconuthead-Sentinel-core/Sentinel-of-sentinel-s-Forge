"""Tests for the RBAC (Role-Based Access Control) system."""
import os
import pytest
from unittest.mock import patch
from fastapi import HTTPException

from backend.core.rbac import (
    Role, resolve_role, register_api_key,
    require_viewer, require_user, require_operator, require_admin,
    _check_role, _ROLE_REGISTRY,
)


@pytest.fixture(autouse=True)
def clean_registry():
    """Clear the role registry between tests."""
    _ROLE_REGISTRY.clear()
    yield
    _ROLE_REGISTRY.clear()


def test_role_hierarchy():
    """Roles have correct ordering."""
    from backend.core.rbac import _ROLE_LEVEL
    assert _ROLE_LEVEL[Role.VIEWER] < _ROLE_LEVEL[Role.USER]
    assert _ROLE_LEVEL[Role.USER] < _ROLE_LEVEL[Role.OPERATOR]
    assert _ROLE_LEVEL[Role.OPERATOR] < _ROLE_LEVEL[Role.ADMIN]


def test_master_key_is_admin():
    """The master API_KEY from settings always resolves to ADMIN."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = "master-secret"
        mock_settings.is_production = False
        role = resolve_role("master-secret")
        assert role == Role.ADMIN


def test_registered_key_resolves():
    """Registered keys resolve to their assigned role."""
    register_api_key("viewer-key-123", Role.VIEWER)
    register_api_key("operator-key-456", Role.OPERATOR)

    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = "master-secret"
        mock_settings.is_production = False
        assert resolve_role("viewer-key-123") == Role.VIEWER
        assert resolve_role("operator-key-456") == Role.OPERATOR


def test_no_key_dev_mode():
    """No key in dev mode defaults to USER."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = ""
        mock_settings.is_production = False
        assert resolve_role(None) == Role.USER


def test_no_key_production_rejects():
    """No key in production raises 401."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = "prod-secret"
        mock_settings.is_production = True
        with pytest.raises(HTTPException) as exc:
            resolve_role(None)
        assert exc.value.status_code == 401


def test_invalid_key_rejects():
    """Unknown key raises 401."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = "master-secret"
        mock_settings.is_production = False
        with pytest.raises(HTTPException) as exc:
            resolve_role("bad-key")
        assert exc.value.status_code == 401


def test_check_role_insufficient():
    """Lower role can't access higher-level endpoints."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = ""
        mock_settings.is_production = False
        # Default dev role is USER, which should fail OPERATOR check
        with pytest.raises(HTTPException) as exc:
            _check_role(None, Role.OPERATOR)
        assert exc.value.status_code == 403


def test_check_role_sufficient():
    """Admin can access all levels."""
    with patch("backend.core.rbac.settings") as mock_settings:
        mock_settings.API_KEY = "admin-key"
        mock_settings.is_production = False
        assert _check_role("admin-key", Role.VIEWER) == Role.ADMIN
        assert _check_role("admin-key", Role.USER) == Role.ADMIN
        assert _check_role("admin-key", Role.OPERATOR) == Role.ADMIN
        assert _check_role("admin-key", Role.ADMIN) == Role.ADMIN
