"""
Symbolic Stream Interpreter
Parses sequences of symbolic/emoji inputs into cognitive operation chains.

Each symbol maps to a Platonic solid primitive and a processing operation.
The interpreter calculates total processing weight and coherence score
(how harmonically consistent the symbol sequence is as a processing pipeline).

Supported symbols:
    💠  → ORIGIN        → origin_align()
    🔺  → TETRAHEDRON   → transform(input)
    🟫  → CUBE          → stable_storage()
    🔷  → DODECAHEDRON  → synthesize(concepts)
    🔶  → OCTAHEDRON    → process_bridges()
    ⭕  → ICOSAHEDRON   → integrate_recursive()

Coherence score: 1 / (1 + frequency_variance)
  — lower variance in processing frequency across the sequence = higher coherence
"""
from __future__ import annotations

from typing import Any, Dict, List

from .cognitive_node import CognitivePrimitiveType


# ---------------------------------------------------------------------------
# Symbol → primitive mapping
# ---------------------------------------------------------------------------

_SYMBOL_MAP: Dict[str, CognitivePrimitiveType] = {
    "💠": CognitivePrimitiveType.ORIGIN,
    "🔺": CognitivePrimitiveType.TETRAHEDRON,
    "🟫": CognitivePrimitiveType.CUBE,
    "🔷": CognitivePrimitiveType.DODECAHEDRON,
    "🔶": CognitivePrimitiveType.OCTAHEDRON,
    "⭕": CognitivePrimitiveType.ICOSAHEDRON,
}

_OPERATION_MAP: Dict[CognitivePrimitiveType, str] = {
    CognitivePrimitiveType.ORIGIN:       "origin_align()",
    CognitivePrimitiveType.TETRAHEDRON:  "transform(input)",
    CognitivePrimitiveType.CUBE:         "stable_storage()",
    CognitivePrimitiveType.DODECAHEDRON: "synthesize(concepts)",
    CognitivePrimitiveType.OCTAHEDRON:   "process_bridges()",
    CognitivePrimitiveType.ICOSAHEDRON:  "integrate_recursive()",
}

_PROCESSING_FREQUENCIES: Dict[CognitivePrimitiveType, float] = {
    CognitivePrimitiveType.ORIGIN:       13.0,
    CognitivePrimitiveType.TETRAHEDRON:   7.83,
    CognitivePrimitiveType.CUBE:          6.66,
    CognitivePrimitiveType.DODECAHEDRON: 11.11,
    CognitivePrimitiveType.OCTAHEDRON:    8.14,
    CognitivePrimitiveType.ICOSAHEDRON:   9.63,
}


class SymbolicStreamInterpreter:
    """
    Interprets a string of emoji/symbols as a cognitive processing chain.
    Unknown characters are silently skipped.
    """

    def __init__(self) -> None:
        self._interpretations: int = 0

    def interpret(self, symbol_sequence: str) -> Dict[str, Any]:
        """
        Parse symbol_sequence and return a full cognitive flow report.

        Returns:
            symbol_sequence         — original input
            cognitive_flow          — per-symbol breakdown
            processing_chain        — human-readable "A → B → C" string
            total_processing_weight — sum of all symbol frequencies
            coherence_score         — harmonic consistency score (0–1)
            interpreted_operations  — list of operation strings
            symbols_recognized      — count of recognised symbols
            symbols_total           — total characters scanned
        """
        self._interpretations += 1
        cognitive_flow: List[Dict[str, Any]] = []
        operations: List[str] = []

        for char in symbol_sequence:
            primitive = _SYMBOL_MAP.get(char)
            if primitive is None:
                continue
            op        = _OPERATION_MAP[primitive]
            frequency = _PROCESSING_FREQUENCIES[primitive]
            operations.append(op)
            cognitive_flow.append({
                "symbol":              char,
                "primitive":           primitive.value,
                "operation":           op,
                "processing_frequency": frequency,
            })

        total_weight = round(sum(f["processing_frequency"] for f in cognitive_flow), 4)
        coherence    = self._coherence(cognitive_flow)

        return {
            "symbol_sequence":         symbol_sequence,
            "cognitive_flow":          cognitive_flow,
            "processing_chain":        " → ".join(operations) or "(no recognized symbols)",
            "total_processing_weight": total_weight,
            "coherence_score":         coherence,
            "interpreted_operations":  operations,
            "symbols_recognized":      len(cognitive_flow),
            "symbols_total":           len(symbol_sequence),
        }

    def suggest_sequence(self, intent: str) -> str:
        """
        Suggest a symbol sequence for a given intent keyword.
        Returns an emoji string.
        """
        intent_lower = intent.lower()
        if "reflect" in intent_lower or "self" in intent_lower:
            return "💠🔺🔷"
        elif "memory" in intent_lower or "store" in intent_lower:
            return "🟫💠🟫"
        elif "recursive" in intent_lower or "feel" in intent_lower:
            return "⭕💠🔶"
        elif "process" in intent_lower or "bridge" in intent_lower:
            return "🔶🔷⭕"
        elif "transform" in intent_lower:
            return "🔺💠🔷"
        return "💠🔺🔶⭕🔷"   # full cognitive cycle

    @property
    def total_interpretations(self) -> int:
        return self._interpretations

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _coherence(cognitive_flow: List[Dict[str, Any]]) -> float:
        if not cognitive_flow:
            return 0.0
        frequencies = [f["processing_frequency"] for f in cognitive_flow]
        mean_f      = sum(frequencies) / len(frequencies)
        variance    = sum((f - mean_f) ** 2 for f in frequencies) / len(frequencies)
        return round(1.0 / (1.0 + variance), 4)


# Module-level singleton
symbol_interpreter = SymbolicStreamInterpreter()
