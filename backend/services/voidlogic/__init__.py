"""
Symbolic Reasoning Engine — multi-layer symbolic processing pipeline
integrated into Sentinel Forge as a first-class cognitive module.

Components:
    node_geometry      — Geometric node tier system (tetrahedral / octahedral / icosahedral)
    context_memory     — Session context memory store
    compute_router     — Compute node router with load balancing
    recursive_feedback — Recursive feedback engine (pattern detection + paradox resolution + emergence)
    tiered_memory      — Tiered memory store with metadata tagging and drift monitoring
    knowledge_bridge   — Cross-domain knowledge bridge threads
    topology_renderer  — Topology visualization layer
    engine             — Master symbolic reasoning orchestration engine
"""

from .engine import SymbolicReasoningEngine

__all__ = ["SymbolicReasoningEngine"]
