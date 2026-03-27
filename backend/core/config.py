import os
import logging
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # --- Core Application ---
    PROJECT_NAME: str = "Sentinel Forge"
    VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"  # development, production
    LOG_LEVEL: str = "INFO"
    API_KEY: str = ""  # Must be set via environment variable or .env file

    # --- CORS ---
    CORS_ORIGINS: str = ""  # Comma-separated allowed origins; empty = allow all in dev only

    # --- Rate Limiting ---
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_RPM: int = 600
    RATE_LIMIT_BURST: int = 120

    # --- AI Provider ---
    AOAI_ENDPOINT: str = ""
    AOAI_KEY: str = ""
    AOAI_CHAT_DEPLOYMENT: str = "gpt-4"
    AOAI_EMBED_DEPLOYMENT: str = "text-embedding-ada-002"
    AOAI_API_VERSION: str = "2024-08-01-preview"
    MOCK_AI: bool = False

    # --- Infrastructure (Cosmos DB) ---
    COSMOS_ENDPOINT: str = "https://localhost:8081/"
    COSMOS_KEY: str = ""
    COSMOS_DATABASE_NAME: str = "SentinelForgeDB"
    COSMOS_CONTAINER_NAME: str = "Items"
    COSMOS_USER_CONTAINER_NAME: str = "Users"

    # --- JWT Authentication ---
    JWT_SECRET_KEY: str = ""  # REQUIRED in production. Generate with: openssl rand -hex 32
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Stripe Billing ---
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_ID_STARTER: str = ""
    STRIPE_PRICE_ID_PRO: str = ""
    STRIPE_PRICE_ID_ENTERPRISE: str = ""

    # --- Performance ---
    RATE_LIMIT_QPS: float = 10.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        """Return parsed CORS origins list."""
        if self.CORS_ORIGINS:
            return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]
        if self.ENVIRONMENT == "production":
            logger.warning("CORS_ORIGINS not set in production — defaulting to no origins allowed")
            return []
        return ["*"]  # Allow all in development

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()


_WEAK_JWT_SECRETS = frozenset({
    "",
    "dev-secret-do-not-use-in-production",
    "secret",
    "changeme",
    "your-secret-key",
})


def validate_security_configuration() -> None:
    """Fail fast when required security settings are missing in production.

    Checks:
      - API_KEY must be set
      - JWT_SECRET_KEY must be set and not a known weak/default value
      - JWT_SECRET_KEY must be at least 32 characters
    """
    if not settings.is_production:
        return

    missing: list[str] = []
    if not settings.API_KEY:
        missing.append("API_KEY")
    if not settings.JWT_SECRET_KEY:
        missing.append("JWT_SECRET_KEY")

    if missing:
        raise RuntimeError(
            "Production configuration missing required secrets: " + ", ".join(missing)
            + ". Set them via environment variables or .env file."
        )

    if settings.JWT_SECRET_KEY.lower().strip() in _WEAK_JWT_SECRETS:
        raise RuntimeError(
            "JWT_SECRET_KEY is set to a known weak/default value. "
            "Generate a strong secret with: openssl rand -hex 32"
        )

    if len(settings.JWT_SECRET_KEY) < 32:
        raise RuntimeError(
            "JWT_SECRET_KEY must be at least 32 characters. "
            "Generate a strong secret with: openssl rand -hex 32"
        )

# Warn at import time if running production without an API key
if settings.is_production and not settings.API_KEY:
    logger.warning(
        "CRITICAL: No API_KEY configured in production. "
        "Set the API_KEY environment variable before deploying."
    )
