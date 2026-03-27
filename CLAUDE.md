# Sentinel Forge — CLAUDE.md

## Project Identity
**Sentinel Forge** is a cognitive AI platform built on the Quantum Nexus Forge (QNF) engine. It provides AI-powered conversation, cognitive processing, knowledge management, and symbolic reasoning — designed for neurodivergent professionals and anyone who needs structured cognitive support.

## Three-Layer Ecosystem (QNF Architecture)

| Layer | Name | Role | Primary Files |
|-------|------|------|---------------|
| **FORGE** | Mind / Software | Backend services, AI, cognition | `backend/` |
| **MAU-1** | Brain / Hardware | QNF engine, pools, scheduling | `quantum_nexus_forge_v5_2_enhanced.py`, `sentinel_cognition.py` |
| **Avatar** | Body / Interface | React SPA, user experience | `frontend-app/src/` |

## Quick Reference

### Run Backend
```bash
cd backend && uvicorn main:app --reload
```

### Run Frontend
```bash
cd frontend-app && npm run dev
```

### Run Tests
```bash
pytest tests/ -v        # 60 tests, all passing
cd frontend-app && npx tsc -b && npm run build  # TypeScript + Vite
```

### Build Docker
```bash
docker compose up --build
```

## Architecture

### Backend (FastAPI)
- **API Router**: `backend/api.py` — 70+ endpoints
- **Auth**: `backend/routes/auth_routes.py` — JWT with bcrypt, RBAC
- **Billing**: `backend/routes/billing_routes.py` — Stripe integration
- **AI Chat**: `backend/services/chat_service.py` — Azure OpenAI / Mock adapter
- **Cognition**: `sentinel_cognition.py` → `SentinelCognitionGraph`
- **Storage**: Cosmos DB → SQLite → in-memory fallback chain
- **Config**: `backend/core/config.py` — env-based, validates JWT at startup

### Frontend (React 18 + TypeScript + Vite)
- **Router**: `App.tsx` — React Router v6, protected routes
- **Auth**: `auth/AuthContext.tsx` — localStorage persistence, auto-refresh
- **API Client**: `lib/api.ts` — typed functions for all backend endpoints
- **Pages**: Chat, Cognition, Notes, Insights, Dashboard, Billing, Settings, Landing

### Key Endpoints
| Route | Purpose |
|-------|---------|
| `/api/auth/*` | Signup, login, refresh, profile |
| `/api/ai/chat` | AI conversation |
| `/api/cog/process` | Cognitive text analysis |
| `/api/cog/memory` | Memory lattice snapshot |
| `/api/cog/rules` | Symbolic rules CRUD |
| `/api/cog/threads` | Thread management |
| `/api/cog/suggest` | AI suggestions |
| `/api/notes/*` | Notes CRUD |
| `/api/glyphs/*` | Glyph system (aliases, pack, interpret, validate, boot) |
| `/api/billing/*` | Stripe plans, checkout, portal |
| `/api/dashboard/*` | Aggregated metrics and activity |
| `/api/metrics/prom` | Prometheus exposition |

## Skills Reference
See `.claude/skills/` for detailed documentation:
- **GRIDMEM-001** — Grid-based contextual memory
- **BLUEPRINT-001** — Architecture blueprint
- **ECOSYSTEM-001** — Component ecosystem mapper
- **SESSION-WRAP-001** — Session persistence
- **NISCOB-001** — Neurodivergent-inclusive design
- **SYM2SPEC-002** — Symbolic-to-specification translator
- **HUBSPOKE-003** — Hub-and-spoke architecture
- **LABDESIGN-004** — Testing framework
- **ZKFS-005** — Privacy & security architecture
- **GDRIVE-006** — External storage integration
- **GLYPH-CODEX-001** — Glyph symbolic language
- **META-PIPELINE** — Pipeline orchestration

## Target Use Cases
1. Neurodivergent professionals (ADHD, autism) — primary audience
2. CNA/Healthcare workers — structured task management
3. Solo entrepreneurs — AI-assisted cognitive offloading
4. Students — study aid with memory lattice
5. Automotive/Trades — reference lookup, procedure notes
6. Elder care — simplified interface, routine support

## Product Modes
- **Conversation Mode** → ChatPage — natural language AI interaction
- **Work Mode** → Dashboard + Cognition + Notes + Insights — structured tools
- **Mode Switching** — ADHD-friendly, no forced context switches

## Pricing Tiers
| Tier | Price | Target |
|------|-------|--------|
| Starter | $29/mo | Individual users |
| Pro | $99/mo | Power users, small teams |
| Enterprise | $499/mo | Organizations |

## Deployment
- Multi-stage Docker (Node build → Python runtime)
- Nginx reverse proxy with SPA fallback
- FastAPI static serving as nginx fallback
- SQLite with WAL mode for persistence without Cosmos
