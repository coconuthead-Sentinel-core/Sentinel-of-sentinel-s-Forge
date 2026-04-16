"""
Enhanced Quantum Nexus Forge v5.2 — Master Cognitive Orchestrator
Combines:
    • SpatialProcessingNode — 3D Platonic solid geometry + processing frequency + entropy
    • SymbolicStreamInterpreter — emoji/symbol sequence → cognitive operations
    • NeurodivergentProcessor — all 5 cognitive lenses (autism/adhd/dyslexia/
                                 dyscalculia/neurotypical) applied in parallel
    • PerformanceMonitor — real-time timing and throughput
    • Zone management — Active / Emergence / Archived memory allocation

Entry point:
    forge = EnhancedQuantumNexusForge()
    result = forge.process(content, symbol_sequence="💠🔺🔶⭕")
    report = forge.system_report()
"""
from __future__ import annotations

import math
import time
import re
from typing import Any, Dict, List, Optional

from .cognitive_node import (
    SpatialProcessingNode,
    CognitivePrimitiveType,
    MemoryZoneClassification,
)
from .symbol_stream import SymbolicStreamInterpreter
from .performance_monitor import PerformanceMonitor


# ---------------------------------------------------------------------------
# Neurodivergent processing — all 5 lenses inlined for standalone operation
# ---------------------------------------------------------------------------

def _autism_lens(content: Any) -> Dict[str, Any]:
    """Autism-spectrum: high-precision micro-pattern recognition."""
    patterns: List[str] = []
    if isinstance(content, str):
        for i in range(len(content) - 2):
            trigram = content[i:i + 3]
            if content.count(trigram) > 1:
                patterns.append(trigram)
    unique_patterns = list(set(patterns))
    return {
        "lens":              "autism_precision_patterns",
        "identified_patterns":  unique_patterns,
        "pattern_count":     len(unique_patterns),
        "pattern_confidence": round(len(patterns) / max(len(str(content)), 1), 4),
        "detail_focus":      "micro_pattern_recognition",
        "processing_depth":  "comprehensive",
    }


def _adhd_lens(content: Any) -> Dict[str, Any]:
    """ADHD: rapid context-switching detection and burst segmentation."""
    switches: List[int] = []
    if isinstance(content, str):
        words = content.split()
        for i, word in enumerate(words):
            if i > 0 and len(word) != len(words[i - 1]):
                switches.append(i)
    return {
        "lens":                 "adhd_dynamic_bursts",
        "context_switch_points": switches,
        "attention_segments":   len(switches) + 1,
        "processing_velocity":  "high_speed_burst",
        "focus_pattern":        "hyperconnected_associations",
    }


_ROTATION_VARIANTS: Dict[str, List[str]] = {
    "b": ["d", "p", "q"], "d": ["b", "p", "q"],
    "p": ["b", "d", "q"], "q": ["b", "d", "p"],
    "n": ["u"],            "u": ["n"],
    "m": ["w"],            "w": ["m"],
}

def _dyslexia_lens(content: Any) -> Dict[str, Any]:
    """Dyslexia: multi-dimensional symbol interpretation and spatial mapping."""
    transformations: Dict[str, List[str]] = {}
    if isinstance(content, str):
        for char in set(content):
            if char.isalpha():
                variants = _ROTATION_VARIANTS.get(char.lower(), [char])
                transformations[char] = variants
    return {
        "lens":                     "dyslexia_symbol_restructuring",
        "symbol_transformations":   transformations,
        "alternative_count":        len(transformations),
        "spatial_cognition":        "three_dimensional_character_mapping",
        "visual_processing":        "holistic_pattern_recognition",
    }


def _prime_factors(n: int) -> List[int]:
    factors: List[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def _visual_groups(n: int) -> str:
    if n <= 10:
        return "●" * n
    groups    = n // 5
    remainder = n % 5
    return "◐" * groups + "●" * remainder


def _magnitude(n: int) -> str:
    if n < 10:    return "single_units"
    if n < 100:   return "double_digit_groups"
    if n < 1000:  return "hundred_magnitude"
    return "thousand_plus_magnitude"


def _dyscalculia_lens(content: Any) -> Dict[str, Any]:
    """Dyscalculia: alternative mathematical reasoning via visual / conceptual representations."""
    numeric_alternatives: Dict[str, Any] = {}
    if isinstance(content, str):
        numbers = [w for w in content.split() if w.isdigit()]
        for num_str in numbers:
            num = int(num_str)
            numeric_alternatives[num_str] = {
                "visual_groups":         _visual_groups(num),
                "prime_factorization":   _prime_factors(num),
                "magnitude":             _magnitude(num),
                "conceptual_pattern":    f"base_10_position_{len(num_str)}",
            }
    return {
        "lens":                    "dyscalculia_alternative_logic",
        "numeric_alternatives":    numeric_alternatives,
        "mathematical_reasoning":  "conceptual_relationship_mapping",
        "quantity_representation": "visual_spatial_quantities",
        "calculation_method":      "pattern_based_estimation",
    }


def _neurotypical_lens(content: Any) -> Dict[str, Any]:
    """Neurotypical baseline: sequential linguistic parsing."""
    return {
        "lens":                 "neurotypical_baseline",
        "linear_analysis":      str(content)[:100],
        "sequential_processing": True,
        "categorization":       "standard_linguistic_parsing",
        "processing_speed":     "moderate_systematic",
    }


_ALL_LENSES = [
    ("autism_precision",     _autism_lens),
    ("adhd_dynamic",         _adhd_lens),
    ("dyslexia_restructure", _dyslexia_lens),
    ("dyscalculia_logic",    _dyscalculia_lens),
    ("neurotypical_baseline",_neurotypical_lens),
]


# ---------------------------------------------------------------------------
# Default symbol sequence
# ---------------------------------------------------------------------------

_DEFAULT_SYMBOLS = "💠🔺🔶⭕🔷"


# ---------------------------------------------------------------------------
# Master forge
# ---------------------------------------------------------------------------

class EnhancedQuantumNexusForge:
    """
    Master cognitive architecture.
    Each call to process() creates a SpatialProcessingNode, runs the full
    symbol stream + all 5 neurodivergent lenses, updates zone managers,
    and returns a rich processing report.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, SpatialProcessingNode] = {}
        self._interpreter   = SymbolicStreamInterpreter()
        self._perf          = PerformanceMonitor()
        self._zone_managers: Dict[MemoryZoneClassification, List[str]] = {
            z: [] for z in MemoryZoneClassification
        }
        self._sessions      = 0
        self.processing_elevation = 40.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(
        self,
        content: Any,
        symbol_sequence: str = _DEFAULT_SYMBOLS,
        primitive_type: CognitivePrimitiveType = CognitivePrimitiveType.CUBE,
    ) -> Dict[str, Any]:
        """
        Run a complete cognitive processing cycle.

        Args:
            content:         Any content (string, dict, list …)
            symbol_sequence: Emoji symbols to interpret as cognitive ops.
            primitive_type:  Override the Platonic solid for this node.

        Returns:
            node_id, symbolic_processing, neurodivergent_analyses,
            spatial_coordinates, entropy, zone, processing_frequency, timing, metrics.
        """
        t0 = time.time()
        self._sessions += 1

        # 1. Create spatial processing node
        node = SpatialProcessingNode(content=content, primitive_type=primitive_type)
        self._nodes[node.id] = node

        # 2. Symbol stream interpretation
        symbolic = self._interpreter.interpret(symbol_sequence)

        # 3. All 5 neurodivergent lenses in parallel (sync; fast)
        nd_analyses: Dict[str, Any] = {}
        for lens_name, lens_fn in _ALL_LENSES:
            nd_analyses[lens_name] = lens_fn(content)

        # 4. Zone management
        zone = node.zone_classification
        self._zone_managers[zone].append(node.id)

        # 5. Performance tracking
        duration = time.time() - t0
        self._perf.record("process", duration)
        self._perf.increment("nodes_created")
        self._perf.increment("symbols_processed",       len(symbol_sequence))
        self._perf.increment("neurodivergent_analyses", len(nd_analyses))
        self._perf.increment("zones_allocated")
        self._perf.increment("forge_sessions")

        return {
            "node_id":                node.id,
            "symbolic_processing":    symbolic,
            "neurodivergent_analyses": nd_analyses,
            "spatial_coordinates":    node.spatial_vector.coordinates,
            "cognitive_elevation":    node.cognitive_elevation,
            "entropy_coefficient":    node.entropy_coefficient,
            "zone_classification":    zone.value,
            "processing_frequency":   round(node.spatial_vector.processing_frequency, 4),
            "processing_timestamp":   node.creation_timestamp.isoformat(),
            "processing_ms":          round(duration * 1000, 3),
            "session":                self._sessions,
        }

    def interpret_symbols(self, symbol_sequence: str) -> Dict[str, Any]:
        """Interpret a symbol sequence without creating a node or running lenses."""
        return self._interpreter.interpret(symbol_sequence)

    def suggest_symbols(self, intent: str) -> Dict[str, Any]:
        """Suggest an emoji symbol sequence for a given intent."""
        seq = self._interpreter.suggest_sequence(intent)
        return {"intent": intent, "suggested_sequence": seq, "interpretation": self._interpreter.interpret(seq)}

    def system_report(self) -> Dict[str, Any]:
        """Return a comprehensive health and metrics report."""
        zone_dist = {z.value: len(ids) for z, ids in self._zone_managers.items()}

        total_processing_weight = sum(
            n.spatial_vector.processing_frequency for n in self._nodes.values()
        )
        avg_entropy = (
            sum(n.entropy_coefficient for n in self._nodes.values()) / len(self._nodes)
            if self._nodes else 0.0
        )

        return {
            "system_status":           "ENHANCED_OPERATIONAL",
            "architecture_version":    "5.2.0",
            "total_cognitive_nodes":   len(self._nodes),
            "zone_distributions":      zone_dist,
            "total_processing_weight": round(total_processing_weight, 4),
            "average_entropy":         round(avg_entropy, 4),
            "processing_elevation":    self.processing_elevation,
            "total_forge_sessions":    self._sessions,
            "available_lenses":        [name for name, _ in _ALL_LENSES],
            "performance":             self._perf.metrics(),
            "health":                  self._assess_health(),
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _assess_health(self) -> Dict[str, Any]:
        score   = 0
        factors: List[str] = []
        total   = len(self._nodes)

        if total > 0:
            active_ratio = (
                len(self._zone_managers[MemoryZoneClassification.ACTIVE_PROCESSING]) / total
            )
            if 0.2 <= active_ratio <= 0.6:
                score += 25; factors.append("zone_balance_optimal")
            else:
                factors.append("zone_balance_suboptimal")

        perf = self._perf.metrics()
        avg  = perf["average_operation_ms"]
        if avg < 50:
            score += 25; factors.append("high_performance")
        elif avg < 200:
            score += 15; factors.append("moderate_performance")
        else:
            factors.append("performance_degradation")

        if perf["processing_counts"]["neurodivergent_analyses"] > 0:
            score += 25; factors.append("neurodivergent_processing_active")

        if total >= 3:
            score += 25; factors.append("adequate_utilization")
        elif total >= 1:
            score += 15; factors.append("minimal_utilization")

        status = (
            "excellent"     if score >= 80 else
            "good"          if score >= 60 else
            "fair"          if score >= 40 else
            "needs_attention"
        )

        return {
            "health_score":   score,
            "health_percent": f"{score}%",
            "health_factors": factors,
            "status":         status,
        }


# Module-level singleton
forge = EnhancedQuantumNexusForge()
