# Portfolio Brief — Sentinel-of-sentinel-s-Forge

> **One-page recruiter overview.** For deep-dive engineering docs see the rest of `docs/` and the [main README](../README.md).

## TL;DR

A production-ready, full-stack **AI orchestration platform** built on FastAPI + Azure OpenAI + Azure Cosmos DB. Designed around a neuro-symbolic cognitive architecture with a three-zone entropy-driven memory system. Demonstrates competence across backend services, async I/O, AI provider integration, authentication, billing, real-time WebSockets, container deployment, and frontend.

## What this project demonstrates

| Capability | Evidence in the codebase |
|---|---|
| **Enterprise backend architecture** | FastAPI app with lifespan management, dependency-injected adapters, repository pattern, domain-driven design (`backend/`) |
| **AI provider integration** | Azure OpenAI adapter with AAD auth (`backend/adapters/azure_openai.py`) and built-in mock for offline dev |
| **Persistent storage** | Azure Cosmos DB repository with mock fallback (`backend/infrastructure/cosmos_repo.py`) |
| **Authentication & authorization** | JWT (python-jose) + bcrypt + role-based access control (`backend/core/auth.py`, `backend/core/rbac.py`) |
| **Subscription billing** | Stripe integration with Starter / Pro / Enterprise tiers (`backend/routes/billing_routes.py`) |
| **Real-time communication** | WebSocket endpoints (`backend/ws_api.py`) |
| **Test discipline** | 9-file pytest suite covering auth, billing, RBAC, config-security, domain, event bus, migrations, vectors, WebSocket |
| **Container deployment** | Dockerfile (Python 3.11-slim, Gunicorn + Uvicorn workers) + docker-compose with nginx reverse proxy |
| **Frontend** | Static HTML/JS dashboard plus Vite + TypeScript app |
| **Operational tooling** | Makefile, PowerShell + Python ops scripts, preflight check, smoke tests, load tester |
| **Security posture** | API-key middleware, JWT secret validation at startup, request-size limits, CORS configuration, structured logging |

## Role categories this project maps to

- **AI Infrastructure Architect** — designed the orchestration layer between LLM providers and persistent storage
- **Backend Engineer (Senior)** — FastAPI, async/await, repository pattern, dependency injection, middleware
- **Healthcare / Compliance-aware Solutions Architect** — local-mode + air-gapped fallbacks, secret-validation gates, structured logging for audit trails
- **DevOps / Platform Engineer** — Docker, nginx, Makefile, CI configuration
- **Full-Stack Developer** — backend + frontend + deployment

## Differentiators

1. **Neurodivergent-first design philosophy.** The cognitive engine is built around accommodating multiple thinking styles, not assuming one default.
2. **Mock-first developer experience.** Engineers can run the full system locally without Azure credentials thanks to in-built mock adapters for both AI and DB.
3. **Repository pattern with clean swap.** Cosmos DB can be replaced with another store by implementing a single repository interface — no business logic changes.
4. **Lifespan-managed warmup.** AAD token warmup, repository initialization, and security validation all run at startup so failures surface immediately rather than mid-request.
5. **Multi-tier subscription billing baked in.** Real Stripe integration with webhook handling, not a stub.

## How to evaluate it in 5 minutes

1. Read [`../README.md`](../README.md) — three ways to run the system
2. Open [`../main.py`](../main.py) — see the FastAPI app composition
3. Open [`../backend/main.py`](../backend/main.py) — see the full lifespan + middleware setup
4. Open [`../backend/core/config.py`](../backend/core/config.py) — see Pydantic-Settings configuration
5. Open [`../tests/test_auth.py`](../tests/test_auth.py) — see test discipline

## How to run it in 60 seconds

```bash
pip install -r ../requirements.txt
cp ../.env.example ../.env       # mock mode is on by default
uvicorn main:app --reload --port 8000
# Visit http://localhost:8000/docs
```

## Author

**Shannon Bryan Kelly** — Neurodivergent AI Architect.  
Built in collaboration with Claude AI (Anthropic).

---

*See [`../POLISH_NOTES.md`](../POLISH_NOTES.md) for the polish-pass changelog.*
