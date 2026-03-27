# HUBSPOKE-003 — Hub-and-Spoke Architecture Pattern

## Purpose
Defines the hub-and-spoke communication pattern used throughout Sentinel Forge. The central hub (FastAPI backend) routes requests to specialized spokes (processors, adapters, repositories).

## Architecture

```
                    ┌─────────────┐
                    │   React SPA │ (Avatar Layer)
                    │   (Hub UI)  │
                    └──────┬──────┘
                           │ HTTP / WebSocket
                    ┌──────▼──────┐
                    │   FastAPI   │ (FORGE Layer)
                    │  (Central   │
                    │    Hub)     │
                    └──┬──┬──┬───┘
                       │  │  │
            ┌──────────┘  │  └──────────┐
            ▼             ▼             ▼
     ┌──────────┐  ┌──────────┐  ┌──────────┐
     │ AI Chat  │  │ Cognition│  │  Notes   │
     │ Service  │  │  Graph   │  │  Repo    │
     │ (Spoke)  │  │ (Spoke)  │  │ (Spoke)  │
     └──────────┘  └──────────┘  └──────────┘
            │             │             │
     ┌──────────┐  ┌──────────┐  ┌──────────┐
     │Azure/Mock│  │  QNF     │  │Cosmos/   │
     │ Adapter  │  │  Engine  │  │ SQLite   │
     └──────────┘  └──────────┘  └──────────┘
```

## Hub Components (Central Router)
- `backend/api.py` — main API router (60+ endpoints)
- `backend/routes/auth_routes.py` — authentication spoke
- `backend/routes/billing_routes.py` — billing spoke
- `backend/main.py` — FastAPI application mount point

## Spoke Components
| Spoke | File | Responsibility |
|-------|------|----------------|
| ChatService | `services/chat_service.py` | AI conversation orchestration |
| CognitionGraph | `sentinel_cognition.py` | Symbolic reasoning, memory, threads |
| QNFService | `service.py` | Processing pools, metrics, events |
| CosmosRepo | `infrastructure/cosmos_repo.py` | Data persistence |
| UserRepo | `infrastructure/user_repository.py` | User account storage |
| EventBus | `eventbus.py` | Async event distribution |
| SyncCoordinator | `sentinel_sync.py` | State synchronization |

## Integration Points
- Each spoke is independently testable
- Adapter pattern allows hot-swapping (Mock ↔ Azure OpenAI)
- Repository pattern allows storage hot-swapping (Cosmos ↔ SQLite ↔ in-memory)
- Event bus decouples spokes from each other

## QNF Ecosystem Layer
**FORGE + MAU-1** — Cross-layer architectural pattern
