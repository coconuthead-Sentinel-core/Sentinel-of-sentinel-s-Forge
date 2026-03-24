import time
from typing import Dict, Optional

from fastapi import Header, HTTPException, WebSocket, status
from starlette.requests import Request

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


def websocket_require_api_key(ws: WebSocket) -> None:
    """Enforce API key for WebSocket connections using header or query param.

    Uses the centralized settings.API_KEY rather than raw env vars.
    Raises HTTPException if auth fails (caller should catch and close the WS).
    """
    if not settings.API_KEY:
        if settings.is_production:
            raise HTTPException(status_code=401, detail="API key required (not configured)")
        return  # Dev mode with no key configured — allow through
    # Try header then query param
    header_val = ws.headers.get("x-api-key")
    query_val = ws.query_params.get("api_key")
    provided = header_val or query_val
    if not provided or provided != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


class RateLimiter:
    """Simple in-memory token bucket per client IP.

    Uses centralized settings rather than raw env vars.
    """

    def __init__(self) -> None:
        self.enabled = settings.RATE_LIMIT_ENABLED
        self.rpm = settings.RATE_LIMIT_RPM
        self.burst = settings.RATE_LIMIT_BURST
        self._buckets: Dict[str, Dict[str, float]] = {}

    def _key(self, request: Request) -> str:
        client = request.client.host if request.client else "unknown"
        return client

    def __call__(self, request: Request) -> None:
        if not self.enabled:
            return
        key = self._key(request)
        now = time.time()
        rate_per_sec = max(1.0, float(self.rpm)) / 60.0
        b = self._buckets.get(key)
        if b is None:
            b = {"tokens": float(self.burst), "ts": now}
        # Refill
        elapsed = max(0.0, now - float(b.get("ts", now)))
        tokens = min(float(b.get("tokens", 0.0)) + elapsed * rate_per_sec, float(self.burst))
        if tokens < 1.0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        tokens -= 1.0
        b["tokens"] = tokens
        b["ts"] = now
        self._buckets[key] = b
