# System Design Document
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026

---

## 1. Architecture Overview

```
[ User / Python CLI ]
       |
       | Direct import or demo.py
       ↓
[ quantum_nexus_forge_v5_2_enhanced.py — Main Engine ]
       |
       ├── CognitiveLensProcessor    — Selects and applies lens
       │     ├── ADHD Lens           — Rapid burst processing
       │     ├── Autism Lens         — Precision pattern recognition
       │     ├── Dyslexia Lens       — Multi-dimensional symbol interpretation
       │     └── Neurotypical Lens   — Baseline processing
       │
       ├── ThreeZoneMemory           — GREEN / YELLOW / RED filing
       ├── GlyphProcessor            — Emoji sequence → cognitive operation
       ├── SpatialCognition          — 3D coordinate mapping
       └── PerformanceMonitor        — Real-time metrics tracking
```

---

## 2. Module Boundaries

| Module | File | Responsibility |
|--------|------|----------------|
| Main engine | `quantum_nexus_forge_v5_2_enhanced.py` | Core cognitive architecture |
| Demo | `demo.py` | Demonstration script for testing |
| Backend | `backend/` | Extended FastAPI backend (optional) |
| Frontend | `frontend/` | Web dashboard |
| Evaluation | `evaluation/` | Performance testing pipeline |
| Tests | `tests/` | Unit test suite |
| Scripts | `scripts/` | Utilities, smoke tests, init scripts |
| Config | `.env` | Credentials and configuration |

---

## 3. Key Data Structures

### Cognitive Processing Result
```python
{
  "lens": "adhd",
  "input": "user input text",
  "concepts": ["quantum", "pattern", "emergence"],
  "spatial_coordinates": [0.7, 0.3, 0.9],
  "entropy": 0.847,
  "zone": "GREEN",
  "response": "processed output text",
  "timestamp": "2026-04-10T15:22:00"
}
```

### Three-Zone Memory Node
```python
{
  "id": "node_sentinel_001",
  "content": "processed concept",
  "entropy": 0.72,
  "zone": "GREEN",   # GREEN > 0.7 | YELLOW 0.3-0.7 | RED < 0.3
  "state": "ACTIVE",
  "lens_origin": "adhd"
}
```

### Glyph Sequence
```python
{
  "input": "🌌🔥💫",
  "primitives": ["Dodecahedron", "Tetrahedron", "Icosahedron"],
  "operation": "activation_sequence",
  "spatial_vector": [0.8, 0.6, 0.9]
}
```

---

## 4. Workflows

### Cognitive Processing Flow
```
1. User provides text or glyph sequence input
2. CognitiveLensProcessor selects lens (adhd/autism/dyslexia/neurotypical)
3. Input processed through selected lens:
   - ADHD: rapid burst, context-switching, dynamic chunking
   - Autism: precision pattern matching, detail-first analysis
   - Dyslexia: spatial interpretation, multi-dimensional symbol reading
   - Neurotypical: standard linear processing
4. GlyphProcessor interprets any emoji sequences as cognitive operations
5. SpatialCognition maps output to 3D coordinate space
6. Result filed into ThreeZoneMemory (GREEN/YELLOW/RED by entropy)
7. PerformanceMonitor records metrics
8. Processed result returned to user
```

### Three-Zone Memory Migration
```
Node created → entropy assessed
  entropy > 0.7  → GREEN zone (active processing)
  entropy 0.3-0.7 → YELLOW zone (pattern emergence)
  entropy < 0.3  → RED zone (crystallized storage)

Over time:
  GREEN overflow → oldest node moves to YELLOW (entropy *= 0.8)
  YELLOW overflow → oldest node moves to RED (state = CRYSTALLIZED)
```

---

## 5. Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Missing dependencies | `ImportError` on startup | `requirements.txt` install resolves |
| Azure OpenAI unavailable | Exception in adapter | Falls back to mock mode automatically |
| Invalid glyph sequence | Unrecognized emoji | Returns null operation, logs warning |
| Memory zone overflow | Zone size > max | Automatic node migration to next zone |
| Invalid lens specified | `ValueError` | Defaults to neurotypical lens |

---

## 6. Cognitive Lens Design

### ADHD Lens
- Rapid context-switching between concepts
- Dynamic burst processing for high-entropy inputs
- Short attention windows with frequent reorientation

### Autism Lens
- Precision pattern recognition
- Detail-focused, systematic analysis
- Structured, predictable processing pathways

### Dyslexia Lens
- Multi-dimensional symbol interpretation
- Spatial cognition over linear text processing
- Alternative mathematical reasoning pathways

### Neurotypical Lens
- Standard baseline processing
- Used for comparison and accessibility benchmarking
