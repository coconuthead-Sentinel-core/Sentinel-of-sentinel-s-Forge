# SYM2SPEC-002 — Symbolic-to-Specification Translator

## Purpose
Translates symbolic rules from the cognition engine into actionable specifications. Bridges the gap between abstract symbolic representations (rules, patterns) and concrete system behavior.

## Integration Points
- **Backend**: `/api/cog/rules` — `cog_get_rules()` returns `SymbolicRules { rules: Dict[str, str] }`
- **Backend**: `/api/cog/rules` (POST) — `cog_set_rules()` accepts `SetRulesRequest { rules: Dict[str, str] }`
- **Backend**: `SentinelCognitionGraph` — maintains rule engine with pattern matching
- **Frontend**: `InsightsPage.tsx` — displays rules in a grid with key/value cards
- **Frontend**: `api.ts → cogGetRules()` — typed fetch for `SymbolicRules`

## Rule Format
Rules are key-value pairs where:
- **Key**: symbolic identifier (e.g., `priority_threshold`, `topic_routing`, `memory_weight`)
- **Value**: specification string (e.g., `>0.8 → escalate`, `medical → healthcare_pool`)

## Translation Flow
```
Symbolic Rule (abstract)
  → SYM2SPEC Parser
    → Behavioral Specification (concrete)
      → Applied to Cognition Pipeline
```

## Current Capabilities
- Rules are stored and retrieved via the API
- Rules grid displayed in InsightsPage
- Rules count shown in DashboardPage under "Cognition Engine"
- Rules influence cognitive processing when set

## QNF Ecosystem Layer
**FORGE** (Mind/Software) — Symbolic reasoning infrastructure
