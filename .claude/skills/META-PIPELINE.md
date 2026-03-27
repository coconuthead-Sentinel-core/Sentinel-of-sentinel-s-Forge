# META-PIPELINE — Orchestration & Pipeline Management

## Purpose
The meta-pipeline orchestrates all other skills and services into a coherent processing flow. It defines how data moves through the system from user input to actionable output.

## Pipeline Stages

### 1. Input Capture (Avatar Layer)
- ChatPage: natural language input
- CognitionPage: structured text submission
- NotesPage: knowledge capture with tags

### 2. Authentication Gate (FORGE Layer)
- JWT validation via `api_key_guard`
- RBAC check via role hierarchy
- Token refresh if expired

### 3. Cognitive Processing (FORGE + MAU-1)
```
Input → QNFService.process() → CognitionGraph.process()
                              → Memory Update (GRIDMEM)
                              → Rule Application (SYM2SPEC)
                              → Thread Routing
                              → Topic Classification
```

### 4. AI Enhancement (FORGE Layer)
```
Processed Context → ChatService.process_message()
                  → AI Adapter (Azure OpenAI / Mock)
                  → Response Generation
```

### 5. Storage & Persistence (MAU-1 Layer)
```
Results → CosmosRepo / SQLite (notes, users)
        → JSONStore (QNF state)
        → Memory Lattice (cognitive state)
```

### 6. Output Delivery (Avatar Layer)
- Chat responses with typing indicators
- Structured cognition results
- Dashboard metrics aggregation
- Insight summaries

## Service Orchestration
| Service | Depends On | Produces |
|---------|-----------|----------|
| ChatService | AI Adapter, CogGraph | Chat responses |
| QNFService | QNF Engine, CogGraph | Processing results |
| CosmosRepo | Cosmos DB / SQLite | Persisted data |
| EventBus | All services | Event notifications |
| SyncCoordinator | All storage | Sync snapshots |

## Integration Points
- `backend/main.py` — application startup, middleware chain
- `backend/api.py` — request routing to appropriate service
- `backend/service.py` — QNFService orchestrates MAU-1 operations
- `backend/services/chat_service.py` — AI conversation pipeline
- Frontend `App.tsx` — client-side routing to appropriate page

## Monitoring
- `/api/metrics` — compact JSON metrics
- `/api/metrics/prom` — Prometheus text exposition
- `/api/dashboard/metrics` — aggregated dashboard view
- EventBus status: published/dropped/errors/subscribers

## QNF Ecosystem Layer
**Cross-layer** — Orchestration spanning FORGE, MAU-1, and Avatar
