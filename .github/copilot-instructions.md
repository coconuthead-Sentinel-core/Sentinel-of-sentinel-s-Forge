# Sentinel Forge - AI Coding Agent Instructions

## Architecture Overview

Sentinel Forge is a **Cognitive AI Orchestration Platform** using Domain-Driven Design (DDD):

```
backend/
├── domain/models.py      # Pure Python entities (Note, Entity) - NO DB fields
├── infrastructure/       # Cosmos DB repository with auto Mock DB fallback
├── services/             # ChatService orchestrates: Input → AI → Memory
├── adapters/             # AzureOpenAIAdapter (AAD auth) ↔ MockOpenAIAdapter
├── core/config.py        # ALL env vars via Pydantic Settings
└── api.py                # FastAPI routes: router (general), ai_router (guarded)
```

**Core Data Flow:** `api.py` → `ChatService` → `AI Adapter` → `cosmos_repo` (persist)

## Development Workflows

```powershell
# Full pipeline: starts server, collects responses, runs eval
python scripts/run_full_eval.py

# Manual server (hot reload)
uvicorn backend.main:app --reload --port 8000

# Tests
pytest tests/                    # All tests
python scripts/smoke_test.py     # Integration (requires running server)
```

**Mock Mode (zero external deps):** Set `MOCK_AI=true` in `.env`. Leave `COSMOS_KEY` empty for auto Mock DB.

## Critical Patterns

### Domain Models (`backend/domain/models.py`)
```python
class Note(Entity):
    text: str
    tag: str
    model_config = ConfigDict(extra="ignore")  # REQUIRED: rejects DB fields
```
- **Never** pass `partitionKey` to domain models - handled in `cosmos_repo.py`
- Tests verify this: see `test_note_strict_config()` in `tests/test_domain.py`

### Adding API Endpoints
1. Use `router` (general) or `ai_router` (auto-applies `api_key_guard`)
2. Delegate to services - routes are thin wrappers
3. All routes prefixed `/api` (e.g., `/api/ai/chat`, `/api/notes`)

### Repository Pattern (`backend/infrastructure/cosmos_repo.py`)
- `_mock_db_mode = True` by default - enables offline dev
- Auto-fallback on ANY Cosmos error (missing creds, container, network)
- DB mapping example: `item["partitionKey"] = note.tag`

### AI Adapters
- Both implement same interface: `chat()`, `embeddings()`
- `AzureOpenAIAdapter`: AAD tokens via `AzureCognitiveTokenProvider`, auto-retry 429/5xx
- `MockOpenAIAdapter`: Returns varied `[MOCK]` responses with realistic structure

## Environment Variables

All in `backend/core/config.py` - never scatter env reads:
```python
MOCK_AI: bool = False              # Toggle MockOpenAIAdapter
COSMOS_ENDPOINT: str = "https://localhost:8081/"  # Emulator default
AOAI_ENDPOINT: str = ""            # Azure OpenAI endpoint
API_KEY: str = "secret"            # For api_key_guard
```

## Integration Points

- **Cosmos DB**: Emulator at `localhost:8081`. Graceful fallback if unavailable.
- **Azure OpenAI**: AAD auth (no API key). Uses `DefaultAzureCredential`.
- **EventBus** (`backend/eventbus.py`): Thread-safe pub/sub with topic filtering and overflow policies (`drop`/`latest`/`block`).
- **Client** (`client.py`): `SentinelClient` with session pooling - use for API calls.

## Common Gotchas

1. **Domain models reject extras** - `Note(partitionKey="x")` silently ignores it
2. **Mock DB is ON by default** - Real DB requires `_mock_db_mode = False` + credentials
3. **Adapters need same interface** - New adapters must match `chat()`/`embeddings()` signatures
4. **Evaluation pipeline** - `evaluation/` folder has test queries and response collection scripts
