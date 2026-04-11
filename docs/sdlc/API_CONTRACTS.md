# API / Interface Contracts
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026
**Base URL:** `http://127.0.0.1:8000`
**API Version:** `2025-01-01-preview`
**AI Deployment:** `o4-mini` (Azure OpenAI — sbryank1234-7203-resource)
**Standard:** ISO/IEC 25010 — Software Quality Characteristics

---

## Authentication

Protected routes (prefix `/api/ai/*`) require the API key header:

```
X-API-Key: <API_KEY from .env>
```

Requests to `/api/ai/*` without a valid key return:
```json
{ "detail": "Forbidden" }   // HTTP 403
```

System/health routes (`/api/status`, `/api/healthz`, etc.) are **unauthenticated**.

---

## Core Cognitive AI Endpoints (`/api/ai/*`)

### POST /api/ai/chat

**Purpose:** Primary cognitive chat endpoint. Routes user messages through the selected cognitive lens (ADHD, Autism, Dyslexia, Neurotypical) and the Azure OpenAI o4-mini model.

**Auth:** Required (X-API-Key)

#### Request
```json
{
  "messages": [
    { "role": "system",    "content": "string — system context (optional)" },
    { "role": "user",      "content": "string — user message (required)" }
  ],
  "temperature":           0.7,
  "max_completion_tokens": 1000,
  "profile":               "adhd | autism | dyslexia | neurotypical | null"
}
```

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `messages` | array | Yes | — | min 1 message |
| `messages[].role` | string | Yes | — | `system`, `user`, `assistant` |
| `messages[].content` | string | Yes | — | non-empty |
| `temperature` | float | No | 0.2 | 0.0–2.0 |
| `max_completion_tokens` | integer | No | null | ≥ 1; required for o4-mini |
| `profile` | string | No | null | cognitive lens selector |

#### Response (200 OK)
```json
{
  "id":      "chatcmpl-abc123",
  "model":   "o4-mini",
  "created": 1744300920,
  "choices": [
    {
      "index":         0,
      "message":       { "role": "assistant", "content": "string — AI response" },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens":     120,
    "completion_tokens": 380,
    "total_tokens":      500
  },
  "lens_metadata": {
    "lens":        "adhd",
    "lens_name":   "ADHD Burst Mode",
    "description": "Rapid context-switching, chunked output, action-verb emphasis"
  },
  "latency_ms": 847.3
}
```

#### Errors
| Code | Condition |
|------|-----------|
| 403 | Missing or invalid X-API-Key |
| 400 | Empty messages array |
| 422 | Invalid message role or field type |
| 500 | Azure OpenAI error (falls back to mock if MOCK_AI=true) |

---

### GET /api/ai/profiles

**Purpose:** List all available cognitive lens profiles with metadata.

**Auth:** Required

#### Response (200 OK)
```json
[
  {
    "lens":        "adhd",
    "lens_name":   "ADHD Burst Mode",
    "description": "Rapid context-switching, chunked responses, action emphasis",
    "temperature": 0.9,
    "max_completion_tokens": 600
  },
  {
    "lens":        "autism",
    "lens_name":   "Autism Precision Mode",
    "description": "Systematic, detail-rich, structured categorization",
    "temperature": 0.3,
    "max_completion_tokens": 1200
  },
  {
    "lens":        "dyslexia",
    "lens_name":   "Dyslexia Spatial Mode",
    "description": "Spatial anchors, visual chunking, multi-dimensional encoding",
    "temperature": 0.7,
    "max_completion_tokens": 700
  },
  {
    "lens":        "dyscalculia",
    "lens_name":   "Dyscalculia Alternative Logic Mode",
    "description": "Narrative math, concrete analogies, non-numeric reasoning",
    "temperature": 0.6,
    "max_completion_tokens": 900
  },
  {
    "lens":        "neurotypical",
    "lens_name":   "Neurotypical Baseline",
    "description": "Standard linear processing — baseline for comparison",
    "temperature": 0.7,
    "max_completion_tokens": 1000
  }
]
```

---

## EventMind Endpoints

### POST /api/ai/eventmind/chat

**Purpose:** Chat through the EventMind pipeline (CorePulse → CoreSensor → Triangulation → FulcrumLens → ReturnVector → AI).

**Auth:** Required

#### Request
```json
{
  "messages": [
    { "role": "user", "content": "string — user message" }
  ],
  "temperature":           0.75,
  "max_completion_tokens": 900
}
```

#### Response (200 OK)
```json
{
  "id":      "chatcmpl-em-456",
  "model":   "o4-mini",
  "created": 1744300920,
  "choices": [{ "index": 0, "message": { "role": "assistant", "content": "string" }, "finish_reason": "stop" }],
  "usage":   { "prompt_tokens": 95, "completion_tokens": 340, "total_tokens": 435 },
  "eventmind_analysis": {
    "core_pulse": {
      "score":  0.82,
      "state":  "RESONANT",
      "hum":    "Signal is clear and structured."
    },
    "core_sensor": {
      "urgency_level": "MEDIUM",
      "triggers":      ["pattern", "emergence"]
    },
    "triangulation": {
      "triangulated_score": 0.74,
      "perspectives":       ["logical", "emotional", "systemic"]
    },
    "fulcrum_lens": {
      "reframe":    "Shift from reaction to strategic response.",
      "confidence": 0.88
    },
    "return_vector": {
      "delivery_mode":      "DIRECT",
      "system_prompt_prefix": "string — EventMind system context",
      "alignment_score":    0.79
    },
    "latency_ms": 312.5
  }
}
```

---

### POST /api/ai/eventmind/analyze

**Purpose:** Run the EventMind analysis pipeline without calling the AI model — signal scoring only.

**Auth:** Required

#### Request
```json
{ "messages": [{ "role": "user", "content": "string" }] }
```

#### Response (200 OK)
```json
{
  "core_pulse":     { "score": 0.82, "state": "RESONANT" },
  "core_sensor":    { "urgency_level": "MEDIUM" },
  "triangulation":  { "triangulated_score": 0.74 },
  "fulcrum_lens":   { "reframe": "string", "confidence": 0.88 },
  "return_vector":  { "delivery_mode": "DIRECT", "alignment_score": 0.79 }
}
```

---

## Onset Protocol Endpoints

### POST /api/ai/onset/activate

**Purpose:** Full Onset Protocol activation: Snowflake decomposition → Rainfall ingestion → Mist anticipation → Spherical Memory → Spiderweb paths → AI generation.

**Auth:** Required

#### Request
```json
{
  "messages": [{ "role": "user", "content": "string" }],
  "temperature":           0.6,
  "max_completion_tokens": 1200
}
```

#### Response (200 OK) — includes AI response + Onset report
```json
{
  "id":      "chatcmpl-onset-789",
  "choices": [{ "message": { "role": "assistant", "content": "string" } }],
  "onset_report": {
    "activation": {
      "storage_protocol":   ["Spiderweb", "Sphere"],
      "processing_protocol": ["Snowflake", "Rainfall", "Mist"],
      "system_state":       "OPERATIONAL"
    },
    "snowflake": {
      "flakes": [
        { "dimension": "analytical", "weight": 0.7 },
        { "dimension": "creative",   "weight": 0.5 }
      ]
    },
    "rainfall":  { "stream_id": "uuid", "ingested": true },
    "mist": {
      "anticipated_concepts": ["emergence", "pattern", "resonance"],
      "pattern_detected":     "recursive_structure"
    },
    "memory_layers": { "active": 12, "pattern": 8, "crystal": 5 },
    "network_paths": [{ "path": "A→B→C", "strength": 0.94 }],
    "latency_ms": 428.7
  }
}
```

---

### GET /api/ai/onset/status

**Purpose:** Return current state of all Onset subsystems.

**Auth:** Required

#### Response (200 OK)
```json
{
  "protocol":     "ONSET",
  "version":      "2.0.0",
  "system_state": "OPERATIONAL",
  "subsystems": {
    "spiderweb":       { "nodes": 24, "edges": 67, "active_paths": 5 },
    "spherical_memory": { "active": 12, "pattern": 8, "crystal": 5 },
    "rainfall":        { "total_ingested": 87, "active_streams": 3 },
    "mist_log":        [{ "query": "...", "anticipated": ["...", "..."] }]
  }
}
```

---

## VoidLogic Endpoints

### POST /api/ai/voidlogic/process

**Purpose:** Full VoidLogic 5.0 + IWE pipeline: CNO routing → CRFE feedback → Tesseract storage → A1 Filing → Bridge Wisdom → STVL topology → AI generation.

**Auth:** Required

#### Request
```json
{
  "messages": [{ "role": "user", "content": "string" }],
  "temperature":           0.65,
  "max_completion_tokens": 1000
}
```

#### Response (200 OK)
```json
{
  "id":      "chatcmpl-vl-321",
  "choices": [{ "message": { "role": "assistant", "content": "string" } }],
  "voidlogic_report": {
    "session":           42,
    "complexity":        0.7312,
    "biased_complexity": 0.6821,
    "domain":            "logic | emotion | pattern | system | myth | general",
    "cno": {
      "tier":            "Octahedral",
      "node_count":      6,
      "routing_path":    ["N1","N3","N5"]
    },
    "crfe": {
      "rsml":            { "score": 0.84, "matched_markers": ["recursion", "emergence"] },
      "emergence":       { "amplified": true, "score": 0.79, "emergent_pattern": "fractal_self_reference" },
      "system_health":   "EMERGING"
    },
    "tesseract":         { "stored": true, "cell_id": "uuid", "resonance": 0.84 },
    "a1_filing":         { "tag": "emergence", "domain": "pattern", "confidence": 0.71 },
    "bridge":            { "source": "pattern", "target": "general", "strength": 0.66 },
    "system_health":     "EMERGING",
    "active_overlay":    "STANDARD"
  },
  "topology_snapshot":   { "nodes": 18, "green": 8, "yellow": 6, "red": 4 },
  "latency_ms":          91.4
}
```

---

### POST /api/ai/voidlogic/emerge

**Purpose:** Focused emergence scan — CRFE + Bridge Wisdom, no storage, no AI call.

**Auth:** Required

#### Request
```json
{ "messages": [{ "role": "user", "content": "string" }] }
```

#### Response (200 OK)
```json
{
  "emergence":     { "amplified": true, "score": 0.79, "emergent_pattern": "fractal_self_reference" },
  "rsml":          { "score": 0.84, "matched_markers": ["recursion"] },
  "domain":        "pattern",
  "cross_domain":  { "insight": "string", "bridge_strength": 0.72 },
  "system_health": "EMERGING"
}
```

---

### GET /api/ai/voidlogic/topology

**Purpose:** Full STVL topology render for dashboard / debug.

**Auth:** Required

#### Response (200 OK)
```json
{
  "nodes":     18,
  "green":      8,
  "yellow":     6,
  "red":        4,
  "tiers":     { "tetrahedral": 4, "octahedral": 8, "icosahedral": 6 },
  "timestamp": 1744300920
}
```

---

### GET /api/ai/voidlogic/overlay

**Purpose:** Return current active VoidLogic overlay and all available overlays.

**Auth:** Required

#### Response (200 OK)
```json
{
  "current_overlay":  "STANDARD",
  "complexity_bias":  0.5,
  "a1_confidence":    0.6,
  "system_prompt_modifier": "string"
}
```

---

### POST /api/ai/voidlogic/overlay/activate

**Purpose:** Switch the active VoidLogic overlay.

**Auth:** Required

#### Request
```json
{ "overlay": "STANDARD | MYTHIC | LOGICAL | EMOTIONAL | PATTERN" }
```

#### Response (200 OK)
```json
{ "activated": "MYTHIC", "previous": "STANDARD" }
```

---

## System / Health Endpoints (`/api/*`)

### GET /api/status

**Purpose:** Lightweight health check — unauthenticated.

#### Response (200 OK)
```json
{
  "system_id":          "sentinel-forge-primary",
  "total_pools":        3,
  "total_processors":   12,
  "total_executions":   847,
  "pool_status":        { "pool-0": { "active": true, "size": 5 } },
  "global_bridges":     4,
  "log_entries":        312,
  "platform":           "Sentinel-of-sentinel-s-Forge v5.2.0"
}
```

---

### GET /api/metrics

**Purpose:** Full system metrics snapshot.

#### Response (200 OK)
```json
{
  "uptime_seconds":    3600,
  "total_requests":    847,
  "zone_distribution": { "green": 312, "yellow": 284, "red": 251 },
  "lens_usage": {
    "adhd":        { "count": 220, "percentage": 26.0 },
    "autism":      { "count": 195, "percentage": 23.0 },
    "dyslexia":    { "count": 160, "percentage": 18.9 },
    "dyscalculia": { "count":  85, "percentage": 10.0 },
    "neurotypical": { "count": 187, "percentage": 22.1 }
  },
  "latency_ms":        { "avg": 91.4, "p95": 183.2, "p99": 347.8 },
  "error_rate":        0.008
}
```

---

### GET /api/healthz

**Purpose:** Kubernetes-style liveness probe.

#### Response (200 OK)
```json
{ "status": "ok" }
```

---

### GET /api/readyz

**Purpose:** Kubernetes-style readiness probe. Returns 503 if Azure adapter is unavailable and MOCK_AI=false.

#### Response (200 OK) — ready
```json
{ "status": "ready", "ai_mode": "live" }
```

#### Response (503) — not ready
```json
{ "status": "not_ready", "reason": "Azure OpenAI unreachable" }
```

---

### GET /api/version

**Purpose:** Return version and deployment metadata.

#### Response (200 OK)
```json
{
  "platform":    "Sentinel-of-sentinel-s-Forge",
  "version":     "5.2.0",
  "ai_model":    "o4-mini",
  "ai_endpoint": "https://sbryank1234-7203-resource.cognitiveservices.azure.com/",
  "mock_mode":   false
}
```

---

## Glyph / Symbol Endpoints

### POST /api/glyph/process

**Purpose:** Process an emoji or glyph sequence through the symbolic engine.

#### Request
```json
{ "data": "🌌🔥💫", "pool_id": null }
```

#### Response (200 OK)
```json
{
  "input_id":       "glyph-001",
  "output_id":      "glyph-result-001",
  "result": {
    "matched_glyphs":  ["🌌","🔥","💫"],
    "dominant_glyph":  "🌌",
    "active_tags":     ["cosmic", "activation", "emergence"],
    "match_positions": [0, 1, 2]
  },
  "processing_time": 0.004,
  "pool_used":       "glyph-pool"
}
```

---

### GET /api/glyph/shapes

**Purpose:** Return all registered glyph-to-shape mappings.

#### Response (200 OK)
```json
{
  "🌌": "Dodecahedron",
  "🔥": "Tetrahedron",
  "💫": "Icosahedron",
  "🌊": "Octahedron",
  "🔮": "Cube",
  "⚡": "Pentagram"
}
```

---

## WebSocket Endpoints

All WebSocket connections served from `ws://127.0.0.1:8000`.

### /ws/cognitive

**Purpose:** Combined real-time stream — cognitive zone events + periodic metrics.

```json
// Zone Transition Event
{
  "type": "cognitive.zone_transition",
  "data": {
    "note_id":    "uuid",
    "input_zone":  "active",
    "output_zone": "pattern",
    "entropy":     0.65,
    "timestamp":   1744300920
  }
}

// Periodic Metrics (every 2 seconds)
{
  "type": "cognitive.metrics",
  "data": {
    "total_processed":    847,
    "zone_distribution":  { "green": 312, "yellow": 284, "red": 251 },
    "lens_usage":         { "adhd": 220, "autism": 195 },
    "latency_ms":         91.4,
    "timestamp":          1744300920
  }
}
```

### /ws/metrics

**Purpose:** Performance dashboard data (2-second intervals).

```json
{
  "event":       "metrics_update",
  "latency_ms":  91.4,
  "throughput":  220.3,
  "memory_usage": 68.4,
  "timestamp":   "2026-04-10T15:22:00"
}
```

---

## Cognitive Lens Interface Contract (Internal)

All lens modules in `backend/services/` must implement:

```python
# Module-level constants
SYSTEM_PROMPT: str         # System prompt injected for this lens
GENERATION_PARAMS: dict    # {"temperature": float, "max_completion_tokens": int}

# Module-level function
def metadata() -> dict:
    # Returns: { "lens": str, "lens_name": str, "description": str }

def apply(response_text: str) -> str:
    # Post-processes AI response per lens rules
    # Returns: transformed response string
```

**Lens parameter table:**

| Lens | Temperature | max_completion_tokens |
|------|------------|----------------------|
| adhd | 0.9 | 600 |
| autism | 0.3 | 1200 |
| dyslexia | 0.7 | 700 |
| dyscalculia | 0.6 | 900 |
| neurotypical | 0.7 | 1000 |

---

## Error Handling Standards

| HTTP Code | Meaning | When Used |
|-----------|---------|-----------|
| 200 | Success | All successful requests |
| 400 | Bad Request | Missing required fields, empty messages array |
| 403 | Forbidden | Missing or invalid X-API-Key on /api/ai/* routes |
| 422 | Unprocessable | Invalid field types, constraint violations |
| 500 | Server Error | Unhandled internal exception |
| 503 | Service Unavailable | Azure OpenAI unreachable (readiness probe only) |

**Azure OpenAI failures** are handled at the adapter layer. If `MOCK_AI=false` and Azure is unreachable, the adapter raises an exception which surfaces as HTTP 500 — it does **not** silently fall back. Set `MOCK_AI=true` to guarantee a response in all conditions.

---

## Rate Limits and Constraints

| Constraint | Value |
|-----------|-------|
| Max request body size | 10 MB (enforced by middleware) |
| Max message content length | 10,000 characters |
| Max `max_completion_tokens` | Model-dependent (o4-mini: 65,536) |
| WebSocket connections | Unlimited (resource-constrained) |
| CORS origins | Configurable via `CORS_ORIGINS` in `.env` |
