"""
Role-Based Access Control (RBAC) for Sentinel Forge.

Defines user roles, permissions, and guards for endpoint protection.
"""
import enum
import logging
from typing import Optional

from fastapi import Header, HTTPException, status

from .config import settings

logger = logging.getLogger(__name__)


class Role(str, enum.Enum):
    """User roles with increasing privilege levels."""
    VIEWER = "viewer"       # Read-only access to public endpoints
    USER = "user"           # Standard access: can use AI, create notes, process data
    OPERATOR = "operator"   # Can manage pools, run stress tests, view state
    ADMIN = "admin"         # Full access: teardown, rebuild, upgrade, profile init


# Maps API key prefixes/values to roles.
# In production, this should be backed by a database lookup.
# Format: { "api_key_value": Role }
# For now, the master API_KEY from settings is always ADMIN.
_ROLE_REGISTRY: dict[str, Role] = {}


def register_api_key(api_key: str, role: Role) -> None:
    """Register an API key with a specific role."""
    _ROLE_REGISTRY[api_key] = role
    logger.info("Registered API key ending ...%s as %s", api_key[-4:] if len(api_key) > 4 else "****", role.value)


def resolve_role(api_key: Optional[str]) -> Role:
    """Resolve the role for a given API key.

    - Master API_KEY from settings is always ADMIN.
    - Registered keys return their assigned role.
    - No key in dev mode returns USER (permissive).
    - No key in prod mode raises 401.
    """
    if api_key and settings.API_KEY and api_key == settings.API_KEY:
        return Role.ADMIN

    if api_key and api_key in _ROLE_REGISTRY:
        return _ROLE_REGISTRY[api_key]

    if not api_key:
        if settings.is_production:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required",
            )
        return Role.USER  # Dev mode: default to USER

    # Key provided but not recognized
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key",
    )


# --- Permission hierarchy ---
_ROLE_LEVEL = {
    Role.VIEWER: 0,
    Role.USER: 1,
    Role.OPERATOR: 2,
    Role.ADMIN: 3,
}


def _check_role(api_key: Optional[str], minimum_role: Role) -> Role:
    """Check that the caller has at least the minimum required role."""
    role = resolve_role(api_key)
    if _ROLE_LEVEL[role] < _ROLE_LEVEL[minimum_role]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {minimum_role.value} role or higher (current: {role.value})",
        )
    return role


# --- FastAPI dependency guards ---

def require_viewer(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> Role:
    """Allow viewers and above."""
    return _check_role(x_api_key, Role.VIEWER)


def require_user(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> Role:
    """Allow users and above."""
    return _check_role(x_api_key, Role.USER)


def require_operator(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> Role:
    """Allow operators and above."""
    return _check_role(x_api_key, Role.OPERATOR)


def require_admin(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> Role:
    """Allow only admins."""
    return _check_role(x_api_key, Role.ADMIN)
