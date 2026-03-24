# Quantum Nexus Forge

**AI that processes information using diverse cognitive patterns**

An enterprise-grade cognitive architecture that processes information using diverse processing modes - making AI systems accessible to diverse thinkers instead of assuming everyone thinks the same way.

## 🎯 What It Does

Traditional AI assumes everyone thinks the same way. This framework includes specialized processing modes for:

- **Rapid Context-Switching Processing Mode:** Rapid context-switching and dynamic bursts
- **Precision Pattern Recognition Processing Mode:** Precision pattern recognition and detail focus  
- **Multi-dimensional Symbol Interpretation Processing Mode:** Multi-dimensional symbol interpretation
- **Alternative Mathematical Reasoning Processing Mode:** Alternative mathematical reasoning

**The Result:** AI systems that adapt to how YOU think, not the other way around.

## 💡 Why It Matters

Most AI tools ignore this entirely, creating accessibility barriers. This framework proves AI can be built inclusively from the ground[...]

**Potential Applications:** 
- Accessible knowledge management systems
- Cognitive-diversity-aware AI assistants  
- Enterprise tools for diverse teams
- Research into computational models of different thinking styles

## 🚀 Tech Stack

- **Backend:** FastAPI + Uvicorn/Gunicorn, WebSockets
- **Language:** Python 3.11+
- **LLM/AI:** OpenAI / Azure OpenAI adapters with mock fallback
- **Data:** Azure Cosmos DB with automatic mock JSON fallback
- **Frontend:** Vanilla JS + HTML (static pages in `/frontend`)
- **Containerization:** Docker & docker-compose
- **Testing:** Pytest + helper scripts in `/scripts`

## 📦 Quick Start
```bash
# Clone the repository
git clone https://github.com/coconuthead-Sentinel-core/Sentinel-of-sentinel-s-Forge.git
cd Sentinel-of-sentinel-s-Forge

# Install dependencies  
pip install -r requirements.txt

# Run the demo
python quantum_nexus_forge_v5_2_enhanced.py
```

## ✨ Core Features

### Three-Zone Memory System
- **🟢 Active Processing:** High-entropy real-time data (>0.7 entropy)
- **🟡 Pattern Emergence:** Mid-entropy pattern recognition (0.3-0.7 entropy)
- **🔴 Crystallized Storage:** Low-entropy stable memory (<0.3 entropy)

### Specialized Processing Modes
- Precision pattern recognition modes
- Dynamic burst processing modes
- Multi-dimensional symbol interpretation modes
- Alternative mathematical reasoning modes
- Standard baseline (for comparison)

### Advanced Capabilities
- **Symbolic Stream Processing:** Interpret emoji sequences as cognitive operations
- **Performance Monitoring:** Real-time metrics and system health tracking
- **Spatial Cognition:** 3D coordinate system with cognitive elevation
- **Geometric Primitives:** Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron

## 📁 Project Structure
Top-level layout (key files only):
```
Sentinel-of-sentinel-s-Forge/
├── backend/                     # FastAPI service
│   ├── api.py                   # REST routes (status, cognition, stress, glyphs)
│   ├── ws_api.py                # WebSocket routes (/ws/sync, /ws/metrics)
│   ├── main.py                  # FastAPI app factory
│   ├── core/                    # Config & security (API key guards, settings)
│   ├── domain/                  # Domain models (Note, MemorySnapshot, etc.)
│   ├── services/                # ChatService, orchestration helpers
│   ├── infrastructure/          # Cosmos DB repository with mock fallback
│   └── adapters/                # Azure/OpenAI adapters (AAD token handling)
├── frontend/                    # Simple JS/HTML demo UI
├── scripts/                     # Dev utilities (load, smoke tests, eval runner)
├── evaluation/                  # Benchmark harness & test data
├── tests/                       # Pytest unit tests (event bus, domain, vectors)
├── docs/                        # Additional docs (API, quickstart, roadmap)
├── quantum_nexus_forge_v5_2_enhanced.py  # Core cognitive engine (standalone)
├── sentinel_cognition.py / sentinel_sync.py / sentinel_profile.py
│                               # Supporting cognition/state helpers
├── vector_utils.py              # Shared vector math utilities
├── Dockerfile / docker-compose.yml
└── README.md                    # You are here
```

### How the code is organized
- **API layer (`backend/api.py`, `backend/ws_api.py`)** – Thin HTTP/WS routers that delegate to services and enforce API key guards.
- **Service layer (`backend/services/`)** – Wraps the cognitive engine and LLM adapters; handles chat, embeddings, and coordination.
- **Domain & infrastructure (`backend/domain/`, `backend/infrastructure/`)** – Clean domain entities (no DB fields) and Cosmos DB repository with automatic mock-mode fallback when Cosmos is unavailable.
- **Adapters (`backend/adapters/`)** – Azure OpenAI adapter with AAD token acquisition plus mock adapter for offline dev.
- **Frontend (`/frontend`)** – Static HTML/JS pages that call the API for quick manual testing/demos.
- **Engine (`quantum_nexus_forge_v5_2_enhanced.py`)** – Standalone cognitive engine implementing the multi-zone memory and processing modes; can be run independently of the API.
- **Operational scripts (`/scripts`, `/evaluation`)** – Helpers for seeding data, smoke testing, and running evaluation scenarios.

## 👤 Author

**Shannon Bryan Kelly** (Coconut Head)  
*Neurodivergent AI Architect*

Built in collaboration with Claude AI (Anthropic)

## 📊 Status

**Production-Ready** | **Version:** 5.2.0 | **Last Updated:** November 2025

---

*Making AI accessible to all cognitive styles, one framework at a time.* 🧠✨
