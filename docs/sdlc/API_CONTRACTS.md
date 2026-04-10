# API / Interface Contracts
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026

---

## Python API (Primary Interface)

### CognitiveOrchestrator

```python
from backend.services.cognitive_orchestrator import CognitiveOrchestrator

orchestrator = CognitiveOrchestrator(lens="adhd")
result = orchestrator.process("🌌🔥💫")
```

#### Input
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lens` | string | Yes | `adhd`, `autism`, `dyslexia`, `neurotypical` |

#### process() Input
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | string | Yes | Text or emoji glyph sequence to process |

#### process() Output
```python
{
  "spatial_coordinates": [0.7, 0.3, 0.9],
  "lens": "adhd",
  "concepts": ["quantum", "pattern"],
  "entropy": 0.847,
  "zone": "GREEN",
  "response": "processed output"
}
```

---

## REST API (Optional — Backend Module)

### GET /api/status

**Purpose:** Health check

```json
{
  "status": "operational",
  "version": "5.2.0",
  "architect": "Shannon Bryan Kelly"
}
```

---

### POST /api/chat

**Purpose:** Cognitive processing via REST

#### Input
```json
{
  "message": "string — user input",
  "lens": "adhd | autism | dyslexia | neurotypical"
}
```

#### Output (200 OK)
```json
{
  "response": "string — processed output",
  "lens_applied": "adhd",
  "zone": "GREEN | YELLOW | RED",
  "spatial_coordinates": [0.7, 0.3, 0.9],
  "concepts_extracted": ["quantum", "pattern"]
}
```

---

### GET /api/metrics

**Purpose:** Performance dashboard

```json
{
  "total_processed": 42,
  "zone_distribution": {
    "green": 18,
    "yellow": 14,
    "red": 10
  },
  "active_lens": "adhd",
  "system_uptime": "00:45:22"
}
```

---

### POST /api/glyph/process

**Purpose:** Symbol / emoji sequence interpretation

#### Input
```json
{
  "sequence": "🌌🔥💫"
}
```

#### Output (200 OK)
```json
{
  "primitives": ["Dodecahedron", "Tetrahedron", "Icosahedron"],
  "operation": "activation_sequence",
  "spatial_vector": [0.8, 0.6, 0.9],
  "interpretation": "High-activation emergence pattern"
}
```

---

## WebSocket Events

### /ws/sync — Real-time cognitive state
```json
{
  "event": "state_update",
  "zone_counts": { "green": 18, "yellow": 14, "red": 10 },
  "current_lens": "adhd",
  "timestamp": "15:22:00"
}
```

### /ws/metrics — Live performance
```json
{
  "event": "metrics_update",
  "latency_ms": 45,
  "throughput": 220,
  "memory_usage": 68
}
```

---

## Cognitive Lens Interface Contract

All lenses must implement:
```python
def process(self, input_text: str) -> dict:
    # Returns: { response, concepts, entropy, zone }

def get_spatial_coordinates(self, processed: dict) -> list:
    # Returns: [x, y, z] float coordinates

def classify_zone(self, entropy: float) -> str:
    # Returns: "GREEN" | "YELLOW" | "RED"
```

---

## Error Handling Standards

| HTTP Code | Meaning | When Used |
|-----------|---------|-----------|
| 200 | Success | All successful requests |
| 400 | Bad Request | Missing message, invalid lens |
| 422 | Unprocessable | Invalid glyph sequence |
| 500 | Server Error | Unhandled internal exception |
