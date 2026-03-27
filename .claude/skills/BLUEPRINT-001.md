# BLUEPRINT-001 — Architecture Blueprint & System Design

## Purpose
Defines the architectural blueprint for Sentinel Forge — the three-layer ecosystem, service boundaries, and data flow patterns that govern the entire platform.

## Three-Layer Ecosystem

### Layer 1: FORGE (Mind / Software)
- FastAPI backend with 70+ API routes
- Cognitive processing pipeline (`SentinelCognitionGraph`)
- Memory lattice, symbolic rules, thread management
- AI chat service with adapter pattern (Mock / Azure OpenAI)
- Notes repository (Cosmos DB / SQLite fallback)
- JWT authentication with RBAC role hierarchy

### Layer 2: MAU-1 (Brain / Hardware)
- QuantumNexusForge processing engine
- Pool-based processor management
- Heap scheduling with stale-ratio monitoring
- Event bus for inter-component communication
- Triage tuner with SGD-based P95 optimization
- Prometheus metrics exposition

### Layer 3: Avatar (Body / Interface)
- React 18 + TypeScript + Vite SPA
- Two interaction modes:
  - **Conversation Mode**: ChatPage — voice I/O ready, AI dialogue
  - **Work Mode**: Dashboard, Cognition, Notes, Insights pages
- Mode switching designed for ADHD-friendly UX
- Responsive design, mobile-first

## Integration Points
- **Config**: `backend/core/config.py` — centralized settings with env var overrides
- **Routing**: `backend/api.py` — main router, `backend/routes/` — auth/billing
- **Frontend**: `App.tsx` — React Router v6 with protected routes
- **Deploy**: `Dockerfile` (multi-stage), `docker-compose.yml`, `nginx/nginx.conf`

## Data Flow
```
User → React SPA → nginx → FastAPI → QNFService → CognitionGraph → Memory/Rules/Threads
                                    → ChatService → AI Adapter → Response
                                    → CosmosRepo → Notes/Users
```
