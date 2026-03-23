from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from .config import settings


def api_key_guard(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> None:
    """Require a valid API key for protected endpoints.

    In production, requests without a configured API key are always rejected.
    In development, if no API_KEY is configured, all requests are allowed.
    """
    if not settings.API_KEY:
        if settings.is_production:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server misconfigured: API_KEY not set",
            )
        # Development mode with no key configured — allow through
        return
    if not x_api_key or x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


def admin_guard(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> None:
    """Guard for destructive/admin endpoints. Always requires API key when configured."""
    api_key_guard(x_api_key)
