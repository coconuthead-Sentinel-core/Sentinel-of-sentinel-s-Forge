"""
JWT Authentication System for Sentinel Forge.

Provides user registration, login, token refresh, and JWT middleware.
Uses an in-memory user store for development; swap to Cosmos DB for production.
"""
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, Header, HTTPException, status
import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel, Field

from .config import settings
from .rbac import Role

logger = logging.getLogger(__name__)


# --- Password Hashing (using bcrypt directly) ---

def _hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# --- Pydantic Schemas ---

class UserCreate(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    display_name: str = Field(default="", max_length=100)


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: str
    email: str
    display_name: str
    role: str
    created_at: str
    subscription_tier: str = "free"


# --- In-Memory User Store (replace with Cosmos DB repository in production) ---

class UserRecord:
    """Internal user record."""
    def __init__(
        self,
        user_id: str,
        email: str,
        hashed_password: str,
        display_name: str = "",
        role: Role = Role.USER,
        subscription_tier: str = "free",
        stripe_customer_id: str = "",
    ):
        self.id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.display_name = display_name
        self.role = role
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.subscription_tier = subscription_tier
        self.stripe_customer_id = stripe_customer_id


# In-memory store — swap for CosmosDBRepository in production
_users: dict[str, UserRecord] = {}  # keyed by user_id
_email_index: dict[str, str] = {}   # email -> user_id


# --- User CRUD ---

def create_user(data: UserCreate) -> UserRecord:
    """Register a new user."""
    email_lower = data.email.lower().strip()
    if email_lower in _email_index:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user_id = str(uuid.uuid4())
    hashed_pw = _hash_password(data.password)
    user = UserRecord(
        user_id=user_id,
        email=email_lower,
        hashed_password=hashed_pw,
        display_name=data.display_name or email_lower.split("@")[0],
    )
    _users[user_id] = user
    _email_index[email_lower] = user_id
    logger.info("User registered: %s (id=%s)", email_lower, user_id)
    return user


def authenticate_user(email: str, password: str) -> Optional[UserRecord]:
    """Verify credentials and return user if valid."""
    email_lower = email.lower().strip()
    user_id = _email_index.get(email_lower)
    if not user_id:
        return None
    user = _users.get(user_id)
    if not user or not _verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(user_id: str) -> Optional[UserRecord]:
    """Look up user by ID."""
    return _users.get(user_id)


def update_user_subscription(user_id: str, tier: str, stripe_customer_id: str = "") -> None:
    """Update a user's subscription tier."""
    user = _users.get(user_id)
    if user:
        user.subscription_tier = tier
        if stripe_customer_id:
            user.stripe_customer_id = stripe_customer_id
        logger.info("User %s subscription updated to %s", user_id, tier)


# --- JWT Token Creation ---

def _create_token(data: dict, expires_delta: timedelta) -> str:
    """Create a signed JWT."""
    secret = _get_jwt_secret()
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    to_encode["iat"] = datetime.now(timezone.utc)
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user: UserRecord) -> str:
    """Create a short-lived access token."""
    return _create_token(
        {"sub": user.id, "email": user.email, "role": user.role.value, "type": "access"},
        timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user: UserRecord) -> str:
    """Create a long-lived refresh token."""
    return _create_token(
        {"sub": user.id, "type": "refresh"},
        timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
    )


def create_token_pair(user: UserRecord) -> TokenResponse:
    """Create both access and refresh tokens."""
    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# --- JWT Token Verification ---

def _get_jwt_secret() -> str:
    """Resolve the JWT secret, failing hard in production if unset."""
    if settings.JWT_SECRET_KEY:
        return settings.JWT_SECRET_KEY
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server misconfigured: JWT_SECRET_KEY not set",
        )
    return "dev-secret-do-not-use-in-production"


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    secret = _get_jwt_secret()
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# --- FastAPI Dependencies ---

def get_current_user(authorization: Optional[str] = Header(default=None)) -> UserRecord:
    """Extract and validate the current user from the Authorization header.

    Supports:
      - Bearer <jwt_token>
      - X-API-Key fallback (for backward compat with API key auth)
    """
    if not authorization:
        if not settings.is_production:
            # Dev mode: return a mock user
            return UserRecord(
                user_id="dev-user",
                email="dev@localhost",
                hashed_password="",
                display_name="Developer",
                role=Role.ADMIN,
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Parse "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must be: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(parts[1])

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type (expected access token)",
        )

    user_id = payload.get("sub")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def require_role(minimum_role: Role):
    """Create a dependency that requires a minimum role via JWT."""
    def _guard(user: UserRecord = Depends(get_current_user)) -> UserRecord:
        from .rbac import _ROLE_LEVEL
        if _ROLE_LEVEL.get(user.role, 0) < _ROLE_LEVEL.get(minimum_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {minimum_role.value} role or higher",
            )
        return user
    return _guard
