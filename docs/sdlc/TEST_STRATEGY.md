# Test Strategy
## Sentinel-of-sentinel-s-Forge v5.2.0

**Architect:** Shannon Bryan Kelly
**Implementation:** Claude AI (Anthropic)
**Date:** November 2025 — April 2026

---

## 1. Testing Philosophy

Every cognitive lens must produce verifiable, reproducible output. Tests ensure the neurodivergent processing pipelines behave correctly, that zone assignments are accurate, and that the system remains accessible and reliable for all users.

---

## 2. Test Levels

### Unit Tests — `tests/`

| Test ID | What It Covers | Pass Criteria |
|---------|---------------|---------------|
| UT-001 | `CognitiveLensRouter` initialization | Object created with selected lens |
| UT-002 | ADHD lens processing | Returns response, entropy, zone fields |
| UT-003 | Autism lens processing | Returns precision-pattern response |
| UT-004 | Dyslexia lens processing | Returns spatial/symbol-based response |
| UT-005 | Neurotypical lens processing | Returns baseline response |
| UT-006 | `ThreeZoneMemory` — GREEN filing | entropy > 0.7 → filed to GREEN |
| UT-007 | `ThreeZoneMemory` — YELLOW filing | entropy 0.3–0.7 → filed to YELLOW |
| UT-008 | `ThreeZoneMemory` — RED filing | entropy < 0.3 → filed to RED |
| UT-009 | `GlyphProcessor` — emoji input | Returns primitives and spatial vector |
| UT-010 | `SpatialCognition` — coordinate output | Returns [x, y, z] float list |
| UT-011 | Zone overflow migration | GREEN overflow moves node to YELLOW |
| UT-012 | Invalid lens fallback | Defaults to neurotypical lens |

**Run command:**
```bash
python -m pytest tests/ -v
```

---

### Integration Tests — Manual

| Test ID | Scenario | Steps | Pass Criteria |
|---------|----------|-------|---------------|
| IT-001 | ADHD lens end-to-end | `process("quantum thinking")` with adhd lens | Returns full result dict, zone assigned |
| IT-002 | Glyph sequence processing | Input `"🌌🔥💫"` | Returns 3 primitives, spatial vector |
| IT-003 | REST API `/api/chat` | POST with message + lens | 200 OK, response and zone returned |
| IT-004 | REST API `/api/status` | GET `/api/status` | Returns version and operational status |
| IT-005 | REST API `/api/metrics` | GET `/api/metrics` | Returns zone distribution and uptime |
| IT-006 | REST API `/api/glyph/process` | POST emoji sequence | Returns primitives and interpretation |
| IT-007 | Web dashboard | Open frontend UI | Dashboard loads, metrics display |
| IT-008 | Azure fallback to mock | Remove `.env` credentials | System falls back to mock, no crash |

---

### Evaluation Pipeline — `evaluation/`

| Metric | Target | Current Score |
|--------|--------|---------------|
| Relevance | ≥ 3.8 / 5.0 | **3.97** ✅ |
| Coherence | ≥ 3.8 / 5.0 | **3.94** ✅ |
| Groundedness | ≥ 3.8 / 5.0 | **3.96** ✅ |
| **Overall** | **≥ 3.9 / 5.0** | **3.96** ✅ |

- 80 prompts distributed across all 4 cognitive lenses (20 per lens)
- Evaluation covers lens-specific behavior and cross-lens consistency
- Scores in range 3.94–3.99/5.0 across all lens configurations

**Run command:**
```bash
python evaluation/run_eval.py
```

---

### CI Pipeline — GitHub Actions

**File:** `.github/workflows/python-app.yml`

| Stage | What Runs | Trigger |
|-------|-----------|---------|
| Install | `pip install -r requirements.txt` | Every push to main |
| Unit tests | `pytest tests/` | Every push to main |
| Smoke test | `python demo.py --smoke` (if available) | Every push to main |

CI always runs in mock mode. Azure credentials are never stored in GitHub.

---

## 3. Lens-Specific Test Coverage

### ADHD Lens Tests
- Rapid burst processing: input with multiple concepts returns multiple concepts extracted
- Context-switching: output shifts topic appropriately for high-entropy input
- Zone distribution: ADHD inputs weighted toward GREEN zone

### Autism Lens Tests
- Pattern precision: structured inputs return systematic, detail-rich responses
- Predictability: same input returns consistent response structure
- Zone distribution: low-entropy structured inputs file to RED (crystallized)

### Dyslexia Lens Tests
- Spatial interpretation: emoji and symbol inputs return richer responses than text-only
- Multi-dimensional output: response includes spatial coordinates
- Alternative reasoning: non-linear input processed without error

### Neurotypical Lens Tests
- Baseline behavior: standard text input returns standard response
- Comparison parity: neurotypical response coherence ≥ all other lenses

---

## 4. Glyph / Emoji Test Data

| Input Sequence | Expected Primitives | Expected Operation |
|---------------|---------------------|--------------------|
| 🌌🔥💫 | Dodecahedron, Tetrahedron, Icosahedron | activation_sequence |
| 🌊🌀⚡ | Variable by mapping | emergence_pattern |
| 🧠💡🔮 | Variable by mapping | cognitive_synthesis |

---

## 5. Environments

| Environment | AI Mode | Azure Credentials | Purpose |
|-------------|---------|-------------------|---------|
| Local Dev | Mock | Not required | Fast lens iteration |
| Local Live | Live (`MOCK_AI=false`) | Required in `.env` | Full pipeline validation |
| CI (GitHub Actions) | Mock | Not present | Automated regression |
| Accessibility Review | Mock | Not required | Neurodivergent usability check |

---

## 6. Accessibility Test Requirements

Per the Definition of Done — every story must pass accessibility review:

| Check | Requirement |
|-------|-------------|
| Color coding | GREEN/YELLOW/RED zones must be distinguishable without color alone |
| Text chunking | Responses must be chunked, not wall-of-text |
| Screen reader | Dashboard must be navigable by screen reader |
| Cognitive load | ADHD lens output must not exceed 3 concepts per chunk |
| Font size | Frontend minimum 16px base font |

---

## 7. Known Gaps

| Gap | Risk | Mitigation |
|-----|------|------------|
| Azure SDK live scoring not integrated | Evaluation runs in mock | SSF-019 in progress |
| No lens accuracy benchmarking against expert panel | Lens quality unverified externally | SSF-024 planned |
| No Cosmos DB persistence tests | Nodes lost on restart | SSF-025 planned |
| No automated accessibility testing | Manual only | Future: axe-core or similar |
| Voice interface not tested | SSF-020 early stage | No tests yet — planned with MVP |

---

## Definition of Test Done

A test is DONE when:
- [ ] Test written and passes locally
- [ ] Lens accuracy validated (if lens-specific test)
- [ ] CI pipeline passes with test included
- [ ] Accessibility impact reviewed
- [ ] No existing tests broken
