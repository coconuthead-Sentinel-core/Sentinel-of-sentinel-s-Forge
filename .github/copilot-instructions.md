# Sentinel Forge - AI Coding Agent Instructions

## Architecture Overview

Sentinel Forge is a **Cognitive AI Orchestration Platform** with two major subsystems:

1. **Backend API** (`backend/`) - FastAPI service using Domain-Driven Design (DDD)
2. **Quantum Nexus Forge** (`quantum_nexus_forge_v5_2_enhanced.py`) - Standalone cognitive engine with neurodivergent processing modes

```
backend/
├── domain/models.py      # Pure Python entities (Note, Entity) - NO DB fields
├── infrastructure/       # Cosmos DB repository with auto Mock DB fallback  
├── services/             # ChatService orchestrates: Input → AI → Memory
├── adapters/             # AzureOpenAIAdapter (AAD auth) ↔ MockOpenAIAdapter
├── core/config.py        # ALL env vars via Pydantic Settings
├── api.py                # REST routes: router (general), ai_router (guarded)
└── ws_api.py             # WebSocket routes: /ws/sync, /ws/metrics
```

**Core Data Flow:** `api.py` → `ChatService` → `AI Adapter` → `cosmos_repo` (persist)

## Development Workflows

```powershell
# Full evaluation pipeline (starts server → collects responses → runs eval)
python scripts/run_full_eval.py

# Manual server (hot reload)
uvicorn backend.main:app --reload --port 8000

# Tests
pytest tests/                    # Unit tests (domain, eventbus, vectors)
python scripts/smoke_test.py     # Integration (requires running server)
```

**Mock Mode (zero external deps):** Set `MOCK_AI=true` in `.env`. Leave `COSMOS_KEY` empty for auto Mock DB.

## Critical Patterns

### Domain Models (`backend/domain/models.py`)
```python
class Note(Entity):
    text: str
    tag: str
    model_config = ConfigDict(extra="ignore")  # REQUIRED: silently ignores DB fields
```
- **Never** pass `partitionKey` to domain models - handled in `cosmos_repo.py`
- Tests verify this: `test_note_strict_config()` in [tests/test_domain.py](tests/test_domain.py)

### Adding API Endpoints
1. Choose router: `router` (public) or `ai_router` (auto-applies `api_key_guard` dependency)
2. Routes are thin wrappers - delegate logic to services
3. All routes prefixed `/api` via main.py (e.g., `/api/ai/chat`, `/api/notes`)

### Repository Pattern (`backend/infrastructure/cosmos_repo.py`)
- `_mock_db_mode = False` default, but auto-enables on ANY Cosmos error
- DB field mapping: `item["partitionKey"] = note.tag` (domain models stay pure)
- Use `cosmos_repo.upsert_note(note)` / `cosmos_repo.get_all_notes()`

### AI Adapters Interface
Both adapters implement identical signatures:
```python
async def chat(deployment, messages, temperature=None, max_tokens=None, ...) -> Dict
async def embeddings(deployment, inputs, dimensions=1536) -> Dict
```
- `AzureOpenAIAdapter`: AAD tokens via `AzureCognitiveTokenProvider`, auto-retry 429/5xx
- `MockOpenAIAdapter`: Returns varied `[MOCK]` responses with OpenAI-compatible structure

## Environment Variables

Centralized in `backend/core/config.py` - never scatter env reads:
```python
MOCK_AI: bool = False              # Toggle MockOpenAIAdapter
COSMOS_ENDPOINT: str               # Azure Cosmos DB or emulator (localhost:8081)
COSMOS_KEY: str                    # Leave empty for auto Mock DB
AOAI_ENDPOINT: str                 # Azure OpenAI endpoint
API_KEY: str = "secret"            # For X-API-Key header validation
```

## Integration Points

- **Cosmos DB**: Emulator at `localhost:8081`. Graceful fallback if unavailable.
- **Azure OpenAI**: AAD auth via `DefaultAzureCredential` (no API key needed)
- **EventBus** (`backend/eventbus.py`): Thread-safe pub/sub with policies: `drop`, `latest`, `block`
- **Client** (`client.py`): `SentinelClient` with session pooling for API integration

## WebSocket Patterns

- Endpoints in `backend/ws_api.py`: `/ws/sync` (state sync), `/ws/metrics` (real-time)
- API key enforcement: `websocket_require_api_key(websocket)` before accept
- EventBus integration: `bus.subscribe(loop, maxsize=1000, policy="latest")`
- Pattern: Send initial snapshot, then stream updates via EventBus queue

## Testing Patterns

- **Unit tests**: Pure logic in `tests/` - domain models, eventbus, vector utils
- **Integration tests**: `scripts/smoke_test.py` (requires running server)
- **Evaluation**: `evaluation/` folder with `test_queries.json` → `collect_responses.py` → `run_evaluation.py`

## Common Gotchas

1. **Domain models reject extras** - `Note(partitionKey="x")` silently ignores it
2. **Mock DB auto-enables** - Any Cosmos error triggers fallback (check logs for `[MOCK DB]`)
3. **Adapters must match interface** - New adapters need identical `chat()`/`embeddings()` signatures
4. **Windows emoji handling** - `scripts/run_full_eval.py` patches stdout for UTF-8

## Code Quality Standards

- **Type hints** - comprehensive typing throughout codebase
- **Async/await** - all I/O operations are async (HTTP, DB, WebSockets)
- **Error handling** - graceful fallbacks (mock DB, mock AI) for offline dev
- **Dependency injection** - services receive adapters via constructor

## Script Import Pattern

Scripts in subdirectories (`scripts/`, `evaluation/`) must add the repo root to `sys.path`:
```python
import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Now imports work
from backend.services.chat_service import ChatService
```

## Actionable Next Steps

**To run the project locally:**
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` (or create with `MOCK_AI=true`)
3. `uvicorn backend.main:app --reload --port 8000`
4. Test: `curl http://localhost:8000/api/status`

**To add a new feature:**
1. Domain model? → `backend/domain/models.py` (use `ConfigDict(extra="ignore")`)
2. API endpoint? → `backend/api.py` (`router` or `ai_router`)
3. Business logic? → `backend/services/` (inject adapters)
4. Database? → `backend/infrastructure/cosmos_repo.py`

**To run evaluation:**
```powershell
python scripts/run_full_eval.py  # Full pipeline
# Or manually:
uvicorn backend.main:app --port 8000 &
python evaluation/collect_responses.py
python evaluation/run_evaluation.py
```
