import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import router as api_router


app = FastAPI(
    title="Quantum Nexus Forge API",
    version="0.1.0",
    description="FastAPI backend exposing QuantumNexusForge operations with a service layer.",
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)


@app.get("/")
async def root():
    return {"service": "Quantum Nexus Forge", "docs": "/docs"}


# CORS: default permissive in dev, restrictive in prod unless configured
env = os.getenv("QNF_ENV", "dev").lower()
default_origins = "*" if env != "prod" else ""
allowed_origins = os.getenv("QNF_CORS_ORIGINS", default_origins)
origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static UI served at /ui; don't fail if directory missing
app.mount("/ui", StaticFiles(directory="frontend", html=True, check_dir=False), name="ui")


# Basic rate limiting middleware (per-IP, in-memory)
_limiter = RateLimiter()

@app.middleware("http")
async def _rate_limit_mw(request: Request, call_next):
    try:
        _limiter(request)
    except Exception as e:
        # If limiter raised an HTTPException, bubble it; else, allow
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            raise e
    return await call_next(request)
