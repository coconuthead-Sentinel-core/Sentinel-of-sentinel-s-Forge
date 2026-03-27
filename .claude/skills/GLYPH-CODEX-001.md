# GLYPH-CODEX-001 — Glyph System & Symbolic Language

## Purpose
Manages the glyph system — Sentinel Forge's symbolic language for compact representation of cognitive operations, boot sequences, and inter-component communication.

## Backend Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/glyphs/aliases` | GET | Get alias mappings for glyph symbols |
| `/api/glyphs/pack` | POST | Pack glyphs into compressed format |
| `/api/glyphs/interpret` | POST | Interpret a glyph sequence into actions |
| `/api/glyphs/validate` | POST | Validate a glyph sequence for correctness |
| `/api/glyphs/boot` | GET | Get boot sequence as glyph steps |

## Schemas
- `GlyphValidateRequest` — input for validation
- `GlyphValidateResponse` — validation result
- `BootStep` — single step in boot sequence (has `glyph` field)

## Service Methods
- `service.glyphs_aliases()` — returns alias mapping dict
- `service.glyphs_pack(payload)` — packs glyph data
- `service.glyphs_interpret(seq)` — interprets glyph sequence string
- `service.glyphs_validate(seq)` — validates glyph sequence
- `service.glyphs_boot()` — returns boot steps

## Data
- `data/glyphs_pack.sample.json` — sample glyph pack definitions
- `sentinel_sync.py` → `_glyphic_signature` — signature verification

## Frontend Integration Gap
The glyph system has full backend support but is **not yet wired** to the frontend. Needs:
1. API client functions in `api.ts` for glyph endpoints
2. A GlyphsPage or section in InsightsPage to display/interact with glyphs
3. Boot sequence visualization

## QNF Ecosystem Layer
**FORGE** (Mind/Software) — Symbolic communication protocol
