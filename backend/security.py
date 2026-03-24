"""
Backward-compatibility shim.

All security utilities are now in backend.core.security.
This module re-exports them so existing imports continue to work.
"""
from .core.security import (  # noqa: F401
    api_key_guard,
    admin_guard,
    websocket_require_api_key,
    RateLimiter,
)
