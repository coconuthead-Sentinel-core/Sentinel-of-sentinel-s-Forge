# System Design Document
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026
**Standard:** ISO/IEC 42010:2022 — Systems and Software Architecture Description

---

## 1. Architecture Overview

```
[ Client — Browser / API Consumer / Evaluation Runner ]
                     |
              REST + WebSocket
                     |
         ┌───────────▼────────────┐
         │  FastAPI Application   │  localhost:8000
         │  backend/main.py       │
         └───┬───────┬────────────┘
             │       │
    ┌─────────▼──┐  ┌▼──────────────────┐
    │ api_router │  │ ai_router          │
    │ /api/*     │  │ /api/ai/*          │
    │ (public)   │  │ (X-API-Key auth)   │
    └─────────┬──┘  └─────────┬──────────┘
              │               │
              │    ┌──────────▼────────────────────────┐
              │    │      CognitiveLensRouter           │
              │    │  backend/services/                 │
              │    │  cognitive_orchestrator.py         │
              │    │                                    │
              │    │  ┌──────────────────┐  ┌────────────────────────┐  │
              │    │  │SignalProcessing   │  │QueryProcessingPipeline │  │
              │    │  │Engine            │  │  protocol.py           │  │
              │    │  └──────────────────┘  └────────────────────────┘  │
              │    │                                    │
              │    │  ┌─────────────────────────────┐  │
              │    │  │  SymbolicReasoningEngine     │  │
              │    │  │  voidlogic/engine.py         │  │
              │    │  │  ComputeNodeRouter→          │  │
              │    │  │  RecursiveFeedbackEngine→    │  │
              │    │  │  ContextMemoryStore→         │  │
              │    │  │  SymbolicMemoryIndex→        │  │
              │    │  │  KnowledgeBridge→            │  │
              │    │  │  TopologyRenderer→           │  │
              │    │  │  OutputTaggingSystem         │  │
              │    │  └─────────────────────────────┘  │
              │    │                                    │
              │    │  Neurodivergent Lens Processor     │
              │    │  ADHD | Autism | Dyslexia |        │
              │    │  Dyscalculia | Neurotypical         │
              │    └────────────┬───────────────────────┘
              │                 │
              │    ┌────────────▼────────────────┐
              │    │  Azure OpenAI Adapter        │
              │    │  backend/adapters/            │
              │    │  azure_openai.py              │
              │    │  Model: o4-mini               │
              │    │  Endpoint: sbryank1234-7203   │
              │    │  API: 2025-01-01-preview      │
              │    │  + Mock fallback              │
              │    └────────────┬────────────────┘
              │                 │
              │    ┌────────────▼────────────────┐
              │    │  Azure Cosmos DB             │
              │    │  infrastructure/cosmos_repo  │
              │    │  (persistence layer)         │
              │    └──────────────────────────────┘
              │
    ┌─────────▼──────────────────────┐
    │  WebSocket Router (ws_router)  │
    │  /ws/cognitive  /ws/metrics    │
    └────────────────────────────────┘
```

---

## 2. Router Architecture

| Router | Prefix | Auth | Purpose |
|--------|--------|------|---------|
| `api_router` | `/api` | None | System health, metrics, notes, glyph processing, COG engine |
| `ai_router` | `/api/ai` | X-API-Key | Cognitive AI: chat, SignalProcessing, QueryProcessing, SymbolicReasoning, Quantum |
| `auth_router` | `/api` | — | JWT authentication endpoints |
| `billing_router` | `/api` | — | Stripe billing endpoints |
| `ws_router` | (root) | None | WebSocket streams: `/ws/cognitive`, `/ws/metrics` |

---

## 3. Module Boundaries

| Module | File(s) | Responsibility |
|--------|---------|---------------|
| FastAPI app | `backend/main.py` | App factory, middleware, router mounting, lifespan |
| API routes | `backend/api.py` | All REST and WebSocket route handlers |
| Schemas | `backend/schemas.py` | Pydantic request/response models |
| CognitiveLensRouter | `backend/services/cognitive_orchestrator.py` | Lens selection → prompt assembly → AI call → post-processing → memory |
| ADHD Lens | `backend/services/adhd_lens.py` | Rapid burst processing, 600 tokens, temperature 0.9 |
| Autism Lens | `backend/services/autism_lens.py` | Precision pattern, 1200 tokens, temperature 0.3 |
| Dyslexia Lens | `backend/services/dyslexia_lens.py` | Spatial/symbol, 700 tokens, temperature 0.7 |
| Dyscalculia Lens | `backend/services/dyscalculia_lens.py` | Alternative math logic, 900 tokens, temperature 0.6 |
| Neurotypical Lens | `backend/services/neurotypical_lens.py` | Baseline, 1000 tokens, temperature 0.7 |
| SignalProcessingEngine | `backend/services/eventmind/engine.py` | SignalStrengthAnalyzer→SignalSensor→MultiPerspectiveAnalyzer→ContextReframer→ResponseRouter |
| QueryProcessingPipeline | `backend/services/onset/protocol.py` | QueryDecomposer→StreamIngester→PredictiveRetriever→MultiLayerMemoryStore→KnowledgeGraph |
| SymbolicReasoningEngine | `backend/services/voidlogic/engine.py` | ComputeNodeRouter→RecursiveFeedbackEngine→ContextMemoryStore→SymbolicMemoryIndex→KnowledgeBridge→TopologyRenderer→OutputTaggingSystem |
| ComputeNodeRouter | `backend/services/voidlogic/cno.py` | Geometric node fabric routing and load balancing |
| RecursiveFeedbackEngine | `backend/services/voidlogic/crfe.py` | Recursive pattern detection, paradox resolution, emergence amplification |
| ContextMemoryStore | `backend/services/voidlogic/tesseract_storage.py` | Multi-dimensional binary-addressed session memory |
| SymbolicMemoryIndex | `backend/services/voidlogic/a1_filing.py` | Tag-based memory filing with drift monitoring |
| CrossDomainBridgeWeaver | `backend/services/voidlogic/bridge_wisdom.py` | Cross-domain knowledge bridge thread reinforcement |
| TopologyRenderer | `backend/services/voidlogic/stvl.py` | Topology visualization data layer |
| OutputTaggingSystem | `backend/services/voidlogic/nexus_tag.py` | Structured metadata auto-tagging |
| OverlayProtocol | `backend/services/voidlogic/overlay_protocol.py` | Processing bias overlay (STANDARD/ANALYTICAL/BALANCED/etc.) |
| Azure OpenAI Adapter | `backend/adapters/azure_openai.py` | Azure OpenAI o4-mini calls, `max_completion_tokens` mapping |
| Mock Adapter | `backend/mock_adapter.py` | Development fallback |
| Cosmos Repository | `backend/infrastructure/cosmos_repo.py` | Note persistence via Azure Cosmos DB |
| Auth | `backend/core/security.py` | JWT + RBAC + API key guard |
| Config | `backend/core/config.py` + `.env` | Environment settings |
| Tests | `tests/` | Unit test suite |
| Evaluation | `evaluation/` | 80-prompt scoring pipeline |
| CI | `.github/workflows/python-app.yml` | Automated build and test |

---

## 4. Key Data Structures

### ChatRequest (Pydantic schema)
```python
{
  "messages":              list[ChatMessage],  # min_length=1
  "temperature":           Optional[float],    # 0.0–2.0, default 0.2
  "max_completion_tokens": Optional[int],      # ≥1, required for o4-mini
  "tools":                 Optional[list],
  "tool_choice":           Optional[str | dict],
  "response_format":       Optional[dict],
  "profile":               Optional[str]       # adhd|autism|dyslexia|dyscalculia|neurotypical
}
```

### ChatResponse (returned to client)
```python
{
  "id":       str,
  "model":    str,    # "o4-mini"
  "created":  int,    # Unix timestamp
  "choices":  [{"index": 0, "message": {"role": "assistant", "content": str}, "finish_reason": str}],
  "usage":    {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int},
  "lens_metadata": {"lens": str, "lens_name": str, "description": str},
  "latency_ms": float
}
```

### Symbolic Reasoning Report
```python
{
  "session":           int,    # increments per call
  "complexity":        float,  # 0–1 from text heuristic
  "biased_complexity": float,  # overlay-adjusted (60/40 blend)
  "domain":            str,    # "logic"|"emotion"|"pattern"|"system"|"narrative"|"general"
  "cno":               dict,   # routing tier, node count, path
  "crfe": {
    "rsml":     {"score": float, "matched_markers": list[str]},
    "emergence": {"amplified": bool, "score": float, "emergent_pattern": str},
    "system_health": "STABLE|AMPLIFIED|EMERGING|CRITICAL"
  },
  "context_memory": {"stored": bool, "cell_id": str, "coherence_score": float},
  "symbolic_memory": {"tag": str, "domain": str, "confidence": float},
  "bridge":          {"source": str, "target": str, "strength": float},
  "system_health": str,
  "active_overlay": str
}
```

### Memory / Note (Cosmos DB record)
```python
{
  "id":   str,       # UUID
  "text": str,       # conversation turn or processed text
  "tag":  str,       # e.g. "chat-history"
  "metadata": {
    "type":       str,    # "conversation"
    "lens":       str,    # lens applied
    "latency_ms": float
  },
  "timestamp": str   # ISO 8601
}
```

---

## 5. Workflows

### Primary Chat Flow (POST /api/ai/chat)
```
1.  Request arrives → api_key_guard validates X-API-Key header
2.  ChatRequest parsed and validated by Pydantic schema
3.  CognitiveLensRouter.process() called with user_message + profile
4.  _resolve_lens(profile) selects lens module (default: neurotypical)
5.  lens.SYSTEM_PROMPT prepended to messages
6.  lens.GENERATION_PARAMS supplies temperature + max_completion_tokens
7.  AzureOpenAIAdapter.chat() called with deployment="o4-mini"
     └─ If MOCK_AI=false: POST to Azure OpenAI 2025-01-01-preview
     └─ If MOCK_AI=true:  Returns mock response string
8.  lens.apply(response_text) post-processes AI output per lens rules
9.  Note saved to Cosmos DB (async, non-blocking; failures are non-fatal)
10. ChatResponse returned with lens_metadata + latency_ms
```

### Symbolic Reasoning Pipeline (POST /api/ai/voidlogic/process)
```
1.  Input text received
2.  _estimate_complexity(text) → float 0–1
3.  _detect_domain(text) → domain string
4.  overlay.get_complexity_bias() → biased_complexity (60/40 blend)
5.  cno.route_payload(text, biased_complexity) → ComputeNodeRouter routing result
6.  crfe.process(text) → RSML score, paradox, emergence, system_health
7.  context_memory.store(content, domain, complexity, coherence_score) → cell_id
8.  a1.file(content, tag, domain, confidence) → symbolic memory record
9.  knowledge_bridge.bridge(domain, "general") → cross-domain thread reinforcement
10. stvl.lite_render() → topology snapshot
11. AzureOpenAIAdapter.complete() called with system prompt from _build_system_prompt()
12. nexus_tag.auto_tag(result) → tags appended
13. Full report returned: ai_response + reasoning_report + topology_snapshot + latency_ms
```

### Signal Processing Pipeline (POST /api/ai/eventmind/chat)
```
1.  SignalStrengthAnalyzer.measure(text)    → score, state, fallback_response
2.  SignalSensor.sense(text)                → urgency_level, triggers
3.  MultiPerspectiveAnalyzer.analyze()      → triangulated_score, perspectives
4.  ContextReframer.reframe(text)           → reframe string, confidence
5.  ResponseRouter.compute(scores...)       → delivery_mode, system_prompt_prefix
6.  If delivery_mode == "SILENT": return fallback_response (no AI call)
7.  Else: AzureOpenAIAdapter.chat() with signal processing system prompt
8.  signal_analysis attached to response
```

### Query Processing Pipeline (POST /api/ai/onset/activate)
```
1.  QueryDecomposer.decompose(text)           → units (query dimensions)
2.  stream_ingester.ingest(text)              → stream_id
3.  predictive_retriever.diffuse(text)        → anticipated_concepts, pattern
4.  multi_layer_store.layer_snapshot()        → memory layer counts
5.  knowledge_graph.strongest_paths(top_n=5) → network path list
6.  Build enriched system_prompt from retriever + decomposition context
7.  AzureOpenAIAdapter.chat() with enriched prompt
8.  pipeline_report attached to response
```

---

## 6. Failure Modes and Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Azure OpenAI unreachable | `httpx.RequestError` in adapter | Raises 500; set `MOCK_AI=true` for guaranteed response |
| Invalid API key | `api_key_guard` dependency | HTTP 403 — "Forbidden" |
| Unknown cognitive profile | `_resolve_lens()` warning | Falls back to neurotypical lens |
| Cosmos DB unavailable | `CosmosHttpResponseError` | Warning logged; response still returned (non-fatal) |
| Max request body exceeded | `RequestSizeLimitMiddleware` | HTTP 413 — "Payload Too Large" |
| WebSocket client disconnects | `WebSocketDisconnect` | Server continues; client reconnects on reload |
| RecursiveFeedbackEngine paradox detected | `system_health == "CRITICAL"` | System prompt modified to include high-complexity reframing |
| Invalid ChatRequest schema | Pydantic `ValidationError` | HTTP 422 — field-level error details returned |

---

## 7. Security Design

| Control | Implementation |
|---------|---------------|
| API key authentication | `api_key_guard` FastAPI dependency on all `/api/ai/*` routes |
| Credential isolation | All keys in `.env`; excluded from GitHub via `.gitignore` |
| Request size limit | `RequestSizeLimitMiddleware` — max 10 MB |
| CORS | Configurable `CORS_ORIGINS` in settings; defaults to localhost |
| HTTPS in production | All Azure communications over TLS 1.2+ |
| JWT auth (planned) | `auth_router` scaffold present; Stripe billing included |
| No persistent user data by default | Cosmos DB write is optional/non-fatal |

---

## 8. Infrastructure Configuration

| Setting | Value |
|---------|-------|
| Runtime | Python 3.11+ |
| Framework | FastAPI + Uvicorn |
| Port | 8000 (default) |
| AI Model | Azure OpenAI o4-mini |
| Azure Resource | sbryank1234-7203-resource.cognitiveservices.azure.com |
| API Version | 2025-01-01-preview |
| Database | Azure Cosmos DB (optional) |
| CI | GitHub Actions (`.github/workflows/python-app.yml`) |
| Container | Docker (`Dockerfile` present) |
