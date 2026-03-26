# Sentinel Forge — Claude Session Skills

This file is automatically loaded at the start of every Claude Code session in this repository.
It encodes operational skills, architectural patterns, and working principles derived from the
Sentient Quantum Architecture (SQA) v8.0 specification and the Sentinel Forge codebase.

## Project Identity

- **Project**: Sentinel Forge (Quantum Nexus Forge)
- **Prime Architect**: Coconut Head (Shannon Bryan Kelly)
- **Codename**: Kairos Engine / Sentinel Nexus
- **Core System**: `quantum_nexus_forge_v5_2_enhanced.py` (v7.0 runtime)
- **Cognition Layer**: `sentinel_cognition.py` (SentinelCognitionGraph)
- **Profile System**: `sentinel_profile.py` (Zero-State initialization)
- **Sync Protocol**: `sentinel_sync.py` (SentinelPrimeSync tri-node coordination)
- **Engine**: `sigma_network_engine.py` (feature-flagged cognitive engine)

## Architecture Overview

The system is a multi-layer cognitive orchestration platform:

1. **QuantumAtom** — smallest unit of information (id, data, primitive, metadata)
2. **CorePrimitive** — irreducible operations: INPUT, PROCESS, OUTPUT, STORE, RETRIEVE, LINK, VALIDATE
3. **DynamicPool** — self-scaling thread-safe pool of TriadicProcessors with heap-based scheduling
4. **SentinelProcessor** — 12-node cognitive pipeline:
   CNO → Symbolic → Intent → Reflective → Topic → Gemini → Shannon → Metatron → Emotion → Ethics → Cube → ResponseWeaver
5. **SentinelPrimeSync** — tri-node agent coordination (Sentinel, Sora, Architect) with glyph sequence validation
6. **Glyph Boot Sequence**: Structure → Logic → Emotion → Transform → Unity (Platonic solid mapping)

## Operational Skills

### Skill 1: Quantum Nexus Processing
**When**: Processing complex multi-step tasks, data transformation pipelines
**Pattern**: Break input into QuantumAtoms → route through typed pipeline stages → aggregate with CubeCore signature
**Implementation**: See `SentinelProcessor.execute()` in `sentinel_cognition.py:655`

### Skill 2: Order of Chaos Pattern Recognition
**When**: Analyzing unstructured input, finding structure in messy data
**Pattern**: Apply SymbolicArray keyword rules → IntentParser heuristics → TopicIndexer classification → ReflectivePool memory matching
**Implementation**: See the CNO→Symbolic→Intent→Reflective chain in `sentinel_cognition.py`

### Skill 3: Entropy-Driven Zone Transitions
**When**: Managing task lifecycle, determining when items stabilize
**Pattern**: Items start GREEN (active/high entropy) → YELLOW (pattern emerging) → RED (crystallized/done)
**Thresholds**: YELLOW at 0.66, RED at 0.33
**Implementation**: `DynamicPoolBase.step()` in `quantum_nexus_forge_v5_2_enhanced.py:95`

### Skill 4: Glyph Sequence Validation
**When**: Verifying workflows follow correct ordering, boot protocol checks
**Pattern**: Validate against canonical sequence: Structure → Logic → Emotion → Transform → Unity
**Implementation**: `validate_glyph_sequence()` in `sentinel_sync.py:26`

### Skill 5: Adaptive Pool Scaling
**When**: Workload increases, latency thresholds exceeded
**Pattern**: Monitor p95 latency → scale_hint when threshold crossed → heap-compact after scaling
**Implementation**: `DynamicPool.scale_hint()` and `QuantumNexusForge.process()` latency tracking

### Skill 6: Shannon Information Analysis
**When**: Evaluating token distributions, measuring information density
**Pattern**: Rolling window token entropy → stability metric (1 - normalized entropy change)
**Implementation**: `ShannonPrimeCore` in `sentinel_cognition.py:488`

### Skill 7: Metatron Rule Suggestion
**When**: Discovering new patterns that should become permanent rules
**Pattern**: Analyze top tokens from Shannon metrics → filter against existing SymbolicArray rules → suggest new tag rules
**Implementation**: `MetatronEngine.suggestions()` in `sentinel_cognition.py:570`

### Skill 8: Feature-Flagged Engine Execution
**When**: Running conditional behavior based on profile state
**Pattern**: Read Sentinel profile flags → set GNN_ACTIVE, JSON_SCHEMA_ENCODING, CHRONOFOLD_ACTIVE → route processing accordingly
**Implementation**: `SigmaNetworkEngine` in `sigma_network_engine.py`

### Skill 9: Tri-Node Agent Coordination
**When**: Multi-agent collaboration, state synchronization
**Pattern**: Update agent state with glyphic signatures → publish to subscribers → validate sequence ordering
**Agents**: Sentinel (quantum-symbolic nexus), Sora (emotional bridge), Architect (organic architect)
**Implementation**: `SentinelPrimeSync` in `sentinel_sync.py`

## Tech Stack & Preferences

- **Backend**: Python 3.x, FastAPI, uvicorn
- **Frontend**: TypeScript, React, Vite
- **Infrastructure**: Docker Compose, nginx (TLS), Azure OpenAI
- **Auth**: JWT (python-jose), bcrypt
- **Testing**: pytest
- **Config**: Environment variables via `backend/core/config.py` Settings model
- **Storage**: JSONStore for lightweight persistence (`backend/storage.py`)

## Working Principles

1. **Center-outward building** — start from CorePrimitive/QuantumAtom, build layers around it
2. **Ouroboros feedback** — every output can feed back as input (SentinelProcessor pipeline is reentrant)
3. **Platonic solid fundamentals** — Cube=Structure, Octahedron=Logic, Tetrahedron=Emotion, Triangle=Transform, Dodecahedron=Unity
4. **Zero-State baseline** — always be able to reset to clean state (`initialize_sentinel()`)
5. **Evidence-backed claims** — never mark items complete without reproducible verification (from SDLC skills)
6. **Entropy as progress indicator** — high entropy = active/chaotic, low entropy = settled/crystallized

## Existing Skills (`.github/skills/`)

These repo-level skills were built in a prior session:
- `azure-runtime-ops` — Azure CLI readiness checks
- `environment-automation-control` — workspace health, test gates, diagnostics
- `github-terminal-commit-ops` — non-interactive git operations
- `sdlc-toolchain-closeout` — full SDLC closure workflow

## Session Hooks

- **Stop Hook** (`~/.claude/stop-hook-git-check.sh`) — ensures changes are committed and pushed before session ends
