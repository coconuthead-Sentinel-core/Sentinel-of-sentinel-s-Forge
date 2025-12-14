import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router, ai_router
from .adapters.azure_openai import AzureCognitiveTokenProvider
from .infrastructure.cosmos_repo import CosmosDBRepository
import uvicorn

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentinel-middleware")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Cosmos DB Repository (will use Mock DB mode if unavailable)
    await CosmosDBRepository.initialize()
    logger.info("Cosmos DB Repository initialized.")

    # Warm up token to fail-fast on bad identity/env.
    provider = AzureCognitiveTokenProvider()
    try:
        await provider.get_token()
        logger.info("AAD token warmup successful.")
    except Exception as exc:
        logger.warning("AAD warmup failed: %s", exc)
    finally:
        await provider.aclose()
    
    yield
    
    # Cleanup on shutdown
    await CosmosDBRepository.close()

app = FastAPI(title="Neurodivergent AI Middleware", lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: Old middleware for request size, rate limiting, and API key are removed.
# New implementation uses dependency injection (`api_key_guard`) and Pydantic settings.

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=75,
        log_level="info"
    )
