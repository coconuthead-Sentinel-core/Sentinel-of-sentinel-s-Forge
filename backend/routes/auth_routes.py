"""
Auth API Routes — Registration, Login, Token Refresh, Profile.

Mount under /api/auth in main.py or api.py.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from ..core.auth import (
    UserCreate,
    UserLogin,
    UserProfile,
    TokenResponse,
    TokenRefreshRequest,
    UserRecord,
    create_user,
    authenticate_user,
    create_token_pair,
    decode_token,
    get_user_by_id,
    get_current_user,
)

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate):
    """Register a new user and return JWT tokens."""
    user = create_user(data)
    return create_token_pair(user)


@auth_router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """Authenticate and return JWT tokens."""
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return create_token_pair(user)


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(data: TokenRefreshRequest):
    """Exchange a refresh token for a new token pair."""
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type (expected refresh token)",
        )
    user = get_user_by_id(payload.get("sub", ""))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return create_token_pair(user)


@auth_router.get("/me", response_model=UserProfile)
async def get_profile(user: UserRecord = Depends(get_current_user)):
    """Get the current user's profile."""
    return UserProfile(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.role.value,
        created_at=user.created_at,
        subscription_tier=user.subscription_tier,
    )
