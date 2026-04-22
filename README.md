# Sentinel Forge Cognitive AI Orchestration Platform

![CI](https://github.com/coconuthead-Sentinel-core/sentinel-forge-cognitive-orchestrator/workflows/Python%20application/badge.svg)

Neurodivergent-aware cognitive orchestration for FastAPI-based chat, symbolic routing, adaptive presentation lenses, and real-time cognitive state streaming.

## Mission
Build an AI orchestration layer that can adapt its output to different cognitive processing styles while keeping the runtime observable, testable, and safe to extend.

## Current Status
- Local validation is green.
- `python -m pytest -q`: `152 passed`
- `python scripts/smoke_test.py`: passed on `2026-04-22`
- Mock AI mode and mock Cosmos persistence both work for local development.
- Azure-backed identity and live model scoring remain optional integrations.
- Engineering-build, SDLC, governance, security, and iOS compliance paperwork packets are now routed through `docs/README.md`.

## Architecture
The current codebase is broader than the original published README. The verified runtime centers on these components:

- `backend/main.py`: FastAPI app bootstrap and router wiring.
- `backend/api.py`: REST endpoints for chat, cognition, glyphs, sync, dashboard, status, jobs, profiles, and operational views.
- `backend/ws_api.py`: WebSocket streams for compatibility sync, cognitive events, and metrics.
- `backend/services/cognitive_orchestrator.py`: Main adaptive processing layer built on `ChatService`, three-zone memory, symbolic metadata, and lens transforms.
- `backend/services/adhd_lens.py`: Chunked, action-oriented formatting.
- `backend/services/autism_lens.py`: Structured detail extraction, definitions, and explicit sectioning.
- `backend/services/dyslexia_lens.py`: Spatial map formatting for visually anchored summaries.
- `backend/services/glyph_processor.py`: Symbolic seed matching and metadata generation.
- `backend/services/glyph_event_bridge.py`: EventBus publication for glyph-driven routing.
- `backend/services/quantum_nexus.py`: Lattice coordinate and dependency resolver used by tests and symbolic workflows.
- `backend/eventbus.py`: In-process event transport for dashboards and WebSockets.
- `backend/infrastructure/cosmos_repo.py`: Cosmos DB repository with mock fallback support for local runs.
- `quantum_nexus_forge_v5_2_enhanced.py` and related top-level modules: lower-level forge/runtime primitives used by orchestration and simulation flows.

## Project Layout
```text
sentinel-forge-cognitive-orchestrator/
|-- backend/
|   |-- api.py
|   |-- main.py
|   |-- ws_api.py
|   |-- eventbus.py
|   |-- services/
|   |-- infrastructure/
|   `-- adapters/
|-- data/
|-- docs/
|-- evaluation/
|-- frontend/
|-- scripts/
|-- static/
|-- templates/
|-- tests/
|-- README.md
|-- requirements.txt
|-- Dockerfile
`-- docker-compose.yml
```

## Quick Start
### Prerequisites
- Python 3.11+
- Optional Azure OpenAI and Cosmos DB credentials if you want live cloud integrations

### Install
```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

### Local development
```powershell
$env:MOCK_AI = "true"
uvicorn backend.main:app --reload --port 8000
```

### Verify the build
```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest -q
```

## Basic Usage
```python
import asyncio

from backend.mock_adapter import MockOpenAIAdapter
from backend.services.cognitive_orchestrator import create_orchestrator


async def main():
    orchestrator = create_orchestrator(MockOpenAIAdapter(), lens="adhd")
    result = await orchestrator.process_message("Explain how glyph routing works.")
    print(result["choices"][0]["message"]["content"])


asyncio.run(main())
```

## Verified API Surface
### REST endpoints
- `GET /api/status`
- `GET /api/metrics`
- `GET /api/healthz`
- `GET /api/readyz`
- `GET /api/version`
- `POST /api/chat`
- `POST /api/glyphs/interpret`
- `POST /api/glyphs/pack`
- `POST /api/glyphs/validate`
- `POST /api/cog/process`
- `GET /api/cog/status`
- `POST /api/activate/{preset}`
- `POST /api/sync/update`
- `GET /api/sync/snapshot`
- `GET /api/sync/trinode`
- `POST /api/notes/upsert`

### WebSocket endpoints
- `/ws/sync`: compatibility stream for raw EventBus forwarding
- `/ws/cognitive`: cognitive and symbolic event stream with initial state snapshot
- `/ws/metrics`: real-time metrics event stream

## Testing
The current automated coverage includes:
- cognitive lens formatting and integration behavior
- glyph loading, fuzzy matching, and bridge emission
- quantum nexus coordinate resolution and dependency tracing
- WebSocket event streaming
- EventBus delivery behavior
- firewall output constraints
- orchestrator symbolic reaction flow

Run the full suite with:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Configuration
### Core environment variables
```bash
MOCK_AI=true
AOAI_ENDPOINT=https://your-endpoint.openai.azure.com/
API_KEY=your-guard-key
COSMOS_ENDPOINT=https://your-account.documents.azure.com/
COSMOS_KEY=your-key
PYTHONPATH=/path/to/project
```

### Runtime notes
- If Azure credentials are absent, local development can still run in mock mode.
- Cosmos persistence falls back to a mock repository in local validation flows.
- Some startup paths still emit FastAPI deprecation warnings around `on_event`; these are warnings, not current test blockers.

## Roadmap
### Completed
- Adaptive cognitive lenses
- Three-zone memory routing
- Symbolic glyph processing
- WebSocket state and metrics streams
- Smoke-testable local development workflow
- Passing automated validation suite

### In progress
- Azure live scoring integration
- deployment hardening and release packaging
- broader documentation cleanup across legacy top-level artifacts

### Future
- additional cognitive lens contributions
- stronger dashboard and observability surfaces
- mobile and voice-facing clients
- research and enterprise integration layers

## Contributing
1. Fork the repository.
2. Create a branch.
3. Install dependencies.
4. Run `python -m pytest -q`.
5. Submit a pull request with clear validation notes.

## License
MIT License. See `LICENSE`.
