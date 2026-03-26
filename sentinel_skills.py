"""
Sentinel Skills Registry — programmatic access to learned operational skills.

Integrates with sentinel_profile.py to inject skills into a Sentinel profile,
and provides standalone query/apply functions for use by the cognition pipeline.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


SKILLS: Dict[str, Dict[str, Any]] = {
    "quantum_nexus_processing": {
        "description": "Multi-step pipeline processing via QuantumAtom routing",
        "trigger": "complex multi-step tasks, data transformation",
        "pattern": "Break input into atoms -> route through typed stages -> aggregate with signature",
        "source": "sentinel_cognition.SentinelProcessor",
    },
    "order_of_chaos": {
        "description": "Finding structure in unstructured input",
        "trigger": "messy data, pattern recognition, classification",
        "pattern": "Symbolic rules -> Intent heuristics -> Topic classification -> Memory matching",
        "source": "sentinel_cognition.CognitiveNeuralOverlay + SymbolicArray + IntentParser + ReflectivePool",
    },
    "entropy_zone_transitions": {
        "description": "Lifecycle management via entropy decay",
        "trigger": "task lifecycle, stabilization detection",
        "pattern": "GREEN (active) -> YELLOW (pattern at 0.66) -> RED (crystallized at 0.33)",
        "source": "quantum_nexus_forge_v5_2_enhanced.DynamicPoolBase",
    },
    "glyph_sequence_validation": {
        "description": "Workflow ordering validation against canonical sequence",
        "trigger": "boot protocol, workflow verification",
        "pattern": "Structure -> Logic -> Emotion -> Transform -> Unity",
        "source": "sentinel_sync.validate_glyph_sequence",
    },
    "adaptive_pool_scaling": {
        "description": "Workload-driven auto-scaling with latency monitoring",
        "trigger": "load increase, p95 latency threshold exceeded",
        "pattern": "Monitor p95 -> scale_hint on threshold -> heap-compact after scaling",
        "source": "quantum_nexus_forge_v5_2_enhanced.DynamicPool",
    },
    "shannon_information_analysis": {
        "description": "Token distribution entropy and stability tracking",
        "trigger": "information density evaluation, content analysis",
        "pattern": "Rolling window entropy -> stability = 1 - normalized entropy change",
        "source": "sentinel_cognition.ShannonPrimeCore",
    },
    "metatron_rule_suggestion": {
        "description": "Automatic discovery of new tagging rules from frequency patterns",
        "trigger": "pattern discovery, rule generation",
        "pattern": "Top tokens from Shannon -> filter vs existing rules -> suggest new tags",
        "source": "sentinel_cognition.MetatronEngine",
    },
    "feature_flagged_execution": {
        "description": "Profile-driven conditional behavior routing",
        "trigger": "mode switching, conditional processing",
        "pattern": "Read profile flags -> set feature toggles -> route processing path",
        "source": "sigma_network_engine.SigmaNetworkEngine",
    },
    "tri_node_coordination": {
        "description": "Multi-agent state sync with glyphic signatures",
        "trigger": "multi-agent collaboration, state synchronization",
        "pattern": "Update state -> glyphic signature -> publish -> validate sequence",
        "source": "sentinel_sync.SentinelPrimeSync",
    },
}


def list_active_skills() -> List[str]:
    """Return names of all registered skills."""
    return list(SKILLS.keys())


def get_skill(name: str) -> Optional[Dict[str, Any]]:
    """Look up a skill by name. Returns None if not found."""
    return SKILLS.get(name)


def apply_skill(name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Apply a named skill to a context dict.

    Returns the context enriched with skill metadata.
    This is a lightweight annotation — actual execution happens
    in the corresponding module referenced by skill['source'].
    """
    skill = SKILLS.get(name)
    if skill is None:
        return {**context, "skill_error": f"Unknown skill: {name}"}
    return {
        **context,
        "active_skill": name,
        "skill_pattern": skill["pattern"],
        "skill_source": skill["source"],
    }


def load_skills_into_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Inject all registered skills into a Sentinel profile dict.

    Adds a 'learned_skills' key containing the full registry,
    compatible with the profile structure from sentinel_profile.py.
    """
    profile["learned_skills"] = {
        name: {
            "description": s["description"],
            "trigger": s["trigger"],
            "pattern": s["pattern"],
        }
        for name, s in SKILLS.items()
    }
    profile["skills_count"] = len(SKILLS)
    return profile
