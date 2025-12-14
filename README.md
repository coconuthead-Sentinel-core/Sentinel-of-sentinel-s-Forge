# Sentinel Forge: Cognitive AI Orchestration Platform

> **Status:** Production Ready v1.0.0 | **Pilot:** VR Studios

**Sentinel Forge** is an enterprise-grade **AI Orchestration Backend** designed to power intelligent, stateful applications. It combines:
- **Neuro-Symbolic Architecture:** Blending LLM creativity with structured logic.
- **Persistent Memory Lattice:** Cosmos DB + Vector Search for long-term recall.
- **Cognitive Pipelines:** Modular services for Chat, Memory, and System Health.

## 🎯 The "Platform" Concept
You are not just building a bot; you have built a **Cognitive Engine**.
- **The Engine:** Sentinel Forge (Backend, API, Database, Logic).
- **The Vehicle:** VR Studios (The first interface/use-case).

This architecture allows you to deploy VR Studios today, and a completely different application tomorrow, using the same brain.

## 🛠️ Core Capabilities
1.  **Multi-Model Support:** Azure OpenAI (GPT-4) with AAD auth or Mock Mode for dev.
2.  **Repository Pattern:** Clean separation between logic and data (Cosmos DB).
3.  **Domain-Driven Design:** Pure Python models independent of infrastructure.
4.  **Observability:** Built-in metrics, dashboards, and health checks.

## 🚀 Quick Start

```bash
# 1. Configure environment
copy .env.example .env

# 2. Run (Production Mode - real Cosmos + OpenAI)
set MOCK_AI=false
python scripts/run_full_eval.py

# 3. Or start server manually
uvicorn backend.main:app --reload --port 8000

# 4. Health check
curl http://127.0.0.1:8000/api/status
```

> **Note:** Cosmos DB Emulator is optional. The system auto-falls back to Mock DB Mode when unavailable.

## 📁 Project Structure

```
backend/
├── domain/models.py      # Pure Python entities (Note, Entity)
├── infrastructure/       # Cosmos DB repository (auto-fallback to mock)
├── services/             # ChatService orchestrates AI pipeline
├── adapters/             # AzureOpenAI ↔ MockOpenAI (swappable)
├── core/config.py        # Centralized settings (Pydantic)
└── api.py                # FastAPI routes: router (general), ai_router (guarded)
```

## 🚀 Deployment Ready

### Azure App Service (Recommended)
1. Containerize: `docker build -t sentinel-forge .`
2. Push to ACR: `az acr build --registry myacr --image sentinel-forge .`
3. Deploy: Use Azure App Service with container support
4. Configure: Set environment variables in App Service settings

### Local Development
- Cosmos DB Emulator: Download from Azure portal
- Azure OpenAI: Set up resource and configure AAD credentials
- Run: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- [Quick Start Guide](docs/QUICKSTART.md)
- [API Examples](docs/API_EXAMPLES.md)
- [Architecture & Git Workflow](docs/GIT_WORKFLOW.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Roadmap](docs/ROADMAP.md)

## 🧪 Testing

```bash
pytest tests/                    # All tests
python scripts/smoke_test.py     # Integration (requires running server)
```

## 📄 License

MIT License - See [THIRD_PARTY_LICENSES.md](docs/THIRD_PARTY_LICENSES.md) for dependencies.

