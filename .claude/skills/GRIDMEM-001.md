# GRIDMEM-001 — Grid-Based Contextual Memory

## Purpose
Structured memory management using grid-based contextual retrieval. Enables the cognitive engine to store, retrieve, and associate memory entries across a spatial grid with semantic proximity.

## Integration Points
- **Backend**: `/api/cog/memory` — `cog_memory_snapshot()` returns `size`, `capacity`, `top_preview[]`
- **Backend**: `/api/cog/memory/clear` — `cog_memory_clear()` resets the memory lattice
- **Backend**: `SentinelCognitionGraph._memory` — in-memory grid with configurable capacity
- **Frontend**: `InsightsPage.tsx` — displays memory entries, capacity, usage percentage
- **Frontend**: `api.ts → cogGetMemory()` — typed fetch for `MemorySnapshot`
- **Schema**: `MemorySnapshot { size, capacity, top_preview[] }`

## Behavior
1. Memory entries are added during cognitive processing (`/api/cog/process`)
2. Entries have semantic weight and topic associations
3. Grid capacity is bounded; oldest/lowest-weight entries are evicted
4. `top_preview` returns the most recent/relevant entries for dashboard display
5. Memory feeds into the suggestion engine for contextual recommendations

## QNF Ecosystem Layer
**FORGE** (Mind/Software) — Core cognitive infrastructure

## Usage
When processing text through the cognition engine, memory entries are automatically created and indexed. The grid structure allows O(1) lookups by topic and O(log n) similarity searches when embeddings are active.
