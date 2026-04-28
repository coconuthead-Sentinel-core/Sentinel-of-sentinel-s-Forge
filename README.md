# Sentinel-of-sentinel-s-Forge

**AI that processes information using diverse cognitive patterns**

An enterprise-grade cognitive architecture that processes information using diverse processing modes — making AI systems accessible to diverse thinkers instead of assuming everyone thinks the same way.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-success)

---

## 🎯 What It Does

Traditional AI assumes everyone thinks the same way. This framework includes specialized processing modes for:

- **Rapid Context-Switching Processing Mode:** dynamic bursts and mode-shifting
- **Precision Pattern Recognition Processing Mode:** detail focus and validation
- **Multi-dimensional Symbol Interpretation Processing Mode:** glyphic and emoji-stream parsing
- **Alternative Mathematical Reasoning Processing Mode:** non-Euclidean cognitive geometries

**The result:** AI systems that adapt to how *you* think, not the other way around.

## 💡 Why It Matters

Most AI tools ignore cognitive diversity entirely, creating accessibility barriers. This framework proves AI can be built inclusively from the ground up.

**Potential applications:**

- Accessible knowledge-management systems
- Cognitive-diversity-aware AI assistants
- Enterprise tools for diverse teams
- Research into computational models of different thinking styles

## 🚀 Tech Stack

- **Language / Framework:** Python 3.11+, FastAPI, async/await
- **AI Provider:** Azure OpenAI (GPT-4) with built-in mock adapter for offline dev
- **Database:** Azure Cosmos DB (with mock fallback)
- **Auth:** JWT (python-jose) + bcrypt + role-based access control
- **Billing:** Stripe subscription tiers (Starter / Pro / Enterprise)
- **Real-time:** WebSockets via FastAPI
- **Frontend:** Vanilla HTML/JS dashboard + Vite/TypeScript app
- **DevOps:** Docker + docker-compose + nginx + Gunicorn / Uvicorn workers
- **Tests:** pytest covering auth, billing, RBAC, config-security, domain, event bus, migrations, vectors, WebSocket
- **Code Quality:** type-hinted, dataclass-driven, repository-pattern, domain-driven design

## 📦 Quick Start

### Option 1 — FastAPI server (recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template and fill values
cp .env.example .env       # (Windows: copy .env.example .env)

# Run with mock AI + mock DB — no Azure account required
uvicorn main:app --reload --port 8000
```

Then open <http://localhost:8000/docs> for the OpenAPI / Swagger UI.

### Option 2 — Standalone cognitive demo

Pure-Python demo of the core cognitive engine, no server required:

```bash
python quantum_nexus_forge_v5_2_enhanced.py
```

### Option 3 — Docker

```bash
docker compose up --build -d
# App: http://localhost:8000   |   nginx: http://localhost:80
```

## ✨ Core Features

### Three-Zone Memory System (entropy-driven)

- 🟢 **Active Processing** — high-entropy real-time data (>0.7 entropy)
- 🟡 **Pattern Emergence** — mid-entropy pattern recognition (0.3 – 0.7 entropy)
- 🔴 **Crystallized Storage** — low-entropy stable memory (<0.3 entropy)

### Specialized Processing Modes

- Precision pattern recognition
- Dynamic burst processing
- Multi-dimensional symbol interpretation
- Alternative mathematical reasoning
- Standard baseline (for comparison)

### Advanced Capabilities

- **Symbolic Stream Processing:** interpret emoji sequences as cognitive operations
- **Performance Monitoring:** real-time metrics, dashboards, health checks
- **Spatial Cognition:** 3D coordinate system with cognitive elevation
- **Geometric Primitives:** Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron
- **Multi-Model Support:** Azure OpenAI or built-in mock adapter
- **Repository Pattern:** clean separation between logic and data
- **Domain-Driven Design:** pure Python models independent of infrastructure

## 📁 Project Structure

```
Sentinel-of-sentinel-s-Forge/
├── main.py                               # FastAPI application entry point
├── quantum_nexus_forge_v5_2_enhanced.py  # Standalone cognitive engine demo
├── sentinel_cognition.py                 # Cognitive layer
├── sentinel_sync.py                      # Sync utilities
├── sentinel_profile.py                   # Profile management
├── sigma_network_engine.py               # Network engine
├── vector_utils.py                       # Vector embedding utilities
├── client.py / dashboard.py / demo_ui.py # UI / demo helpers
│
├── backend/                              # FastAPI service layer
│   ├── main.py                           # Alternate FastAPI entry (with full lifespan)
│   ├── api.py                            # REST endpoints
│   ├── ws_api.py                         # WebSocket endpoints
│   ├── service.py                        # Business logic
│   ├── schemas.py / models.py            # Pydantic + domain models
│   ├── adapters/                         # AI provider adapters (Azure OpenAI, mock)
│   ├── core/                             # Config, auth, RBAC, security, logging
│   ├── routes/                           # Auth + billing routes
│   ├── infrastructure/                   # Cosmos DB + user repository
│   ├── domain/                           # Pure-domain models
│   └── services/                         # Service-layer modules
│
├── frontend/                             # Static dashboard (HTML / JS)
├── frontend-app/                         # Vite + TypeScript app
│
├── tests/                                # pytest suite (9 files)
├── scripts/                              # Ops scripts (PowerShell + Python)
├── docs/                                 # Architecture, API, SDLC, compliance docs
├── data/                                 # Glyph packs + seed data
├── evaluation/                           # Eval harness + test queries / responses
├── enterprise_docs/                      # Enterprise documentation
├── diagrams/                             # Architectural diagrams
│
├── Dockerfile / docker-compose.yml       # Container deployment
├── nginx/                                # Reverse-proxy config
├── Makefile                              # Common ops commands
├── requirements.txt                      # Python dependencies
├── .env.example                          # Environment configuration template
├── POLISH_NOTES.md                       # Recent polish-pass changelog
└── README.md                             # This file
```

## 📚 Documentation

Key references in [`docs/`](docs/):

- [Quickstart](docs/QUICKSTART.md)
- [API Examples](docs/API_EXAMPLES.md)
- [User Guide](docs/USER_GUIDE.md)
- [Roadmap](docs/ROADMAP.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Environment Setup](docs/env_setup.md)
- [SDLC Tools & Skills Blueprint](docs/SDLC_TOOLS_SKILLS_BLUEPRINT.md)
- [Completeness Assessment](docs/COMPLETENESS_ASSESSMENT.md)
- [Release Pipeline](docs/RELEASE_PIPELINE.md)
- [Third-Party Licenses](docs/THIRD_PARTY_LICENSES.md)
- [Portfolio Brief (recruiter overview)](docs/PORTFOLIO_BRIEF.md)

## 🧪 Testing

```bash
pytest -q
```

Coverage includes auth flow, billing webhooks, config-security validation, domain models, event bus, schema migrations, vector utilities, and WebSocket endpoints.

## 🐳 Deployment Commands

```bash
make up        # docker compose build + run
make logs      # tail container logs
make down      # stop containers
make test      # run pytest
make load      # stress test (250 concurrent requests)
```

## 👤 Author

**Shannon Bryan Kelly**  
*Neurodivergent AI Architect*

Built in collaboration with Claude AI (Anthropic).

## 📄 License

[MIT License](MIT%20License) — free to use, modify, distribute.

## 📊 Status

**Production-Ready** | **Version:** 5.2.0 | **Last Updated:** April 2026

---

*Making AI accessible to all cognitive styles, one framework at a time.* 🧠✨
