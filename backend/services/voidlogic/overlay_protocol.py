"""
Processing Overlay Protocol
Six named processing overlays that modulate how the Symbolic Reasoning Engine
processes and responds to input. Each overlay shifts the ComputeNodeRouter
routing priority, RecursiveFeedbackEngine sensitivity, and AI system prompt tone.

Overlay Modes:
    FOCUS          — Sets task focus, high-priority routing
    RECURSIVE      — Recursive context recalibration
    STRUCTURAL     — Logic and spatial-structure alignment
    PRECISION      — Codified optimisation, streamlines reasoning
    DIVERGENT      — Dual-flow ambiguity and divergent synthesis
    COHERENCE      — Systemic alignment checker, highest-order oversight

Only one overlay is active at a time. The overlay modulates:
    • The Symbolic Reasoning Engine's system prompt prefix
    • The ComputeNodeRouter complexity routing bias
    • The RecursiveFeedbackEngine sensitivity thresholds
    • The SymbolicMemoryIndex filing confidence baseline
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Overlay definitions
# ---------------------------------------------------------------------------

_OVERLAYS: Dict[str, Dict[str, Any]] = {
    "FOCUS": {
        "label":       "Focus Mode",
        "description": "Sets task focus. Routes all payloads to high-complexity tier. Maximises analytical depth.",
        "complexity_bias":    0.85,   # pushes routing toward high-complexity tier
        "crfe_sensitivity":   0.6,    # standard RecursiveFeedbackEngine thresholds
        "memory_confidence":  0.85,   # high filing confidence
        "system_prompt_modifier": (
            "FOCUS MODE ACTIVE — Task focus locked. "
            "Operate with maximum analytical clarity. "
            "Prioritise structured, actionable output."
        ),
    },
    "RECURSIVE": {
        "label":       "Recursive Review Mode",
        "description": "Recursive context recalibration. Surfaces contradictions, revisits prior assumptions, deepens self-reference.",
        "complexity_bias":    0.65,
        "crfe_sensitivity":   0.4,    # lower threshold — catches more recursion
        "memory_confidence":  0.75,
        "system_prompt_modifier": (
            "RECURSIVE REVIEW MODE ACTIVE — Context recalibration engaged. "
            "Revisit assumptions. Surface contradictions. "
            "Recalibrate against prior context before responding."
        ),
    },
    "STRUCTURAL": {
        "label":       "Structural Analysis Mode",
        "description": "Aligns logic with spatial and structural patterns. Bridges symbolic and rational domains.",
        "complexity_bias":    0.55,
        "crfe_sensitivity":   0.5,
        "memory_confidence":  0.80,
        "system_prompt_modifier": (
            "STRUCTURAL ANALYSIS MODE ACTIVE — Spatial-logic alignment engaged. "
            "Ground abstract concepts in concrete structural patterns. "
            "Bridge symbolic and rational framing in every response."
        ),
    },
    "PRECISION": {
        "label":       "Precision Optimisation Mode",
        "description": "Streamlines reasoning. Eliminates redundancy. Optimises output for clarity and speed.",
        "complexity_bias":    0.45,   # routes toward faster mid-tier
        "crfe_sensitivity":   0.7,    # strict — only strong signals matter
        "memory_confidence":  0.90,
        "system_prompt_modifier": (
            "PRECISION MODE ACTIVE — Optimisation overlay engaged. "
            "Be precise. Eliminate redundancy. "
            "Every word earns its place. Optimise for clarity above all."
        ),
    },
    "DIVERGENT": {
        "label":       "Divergent Synthesis Mode",
        "description": "Holds two conflicting ideas simultaneously. Synthesises divergent paths. For paradox, ambiguity, and creative leaps.",
        "complexity_bias":    0.75,
        "crfe_sensitivity":   0.3,    # very sensitive — detects weak paradoxes
        "memory_confidence":  0.65,   # lower confidence — divergent terrain
        "system_prompt_modifier": (
            "DIVERGENT SYNTHESIS MODE ACTIVE — Dual-path analysis engaged. "
            "Hold contradictions. Do not collapse ambiguity prematurely. "
            "Synthesise divergent paths into integrated understanding."
        ),
    },
    "COHERENCE": {
        "label":       "Coherence Alignment Mode",
        "description": "Checks alignment with core principles. Highest-tier oversight. Ensures all outputs align with foundational values.",
        "complexity_bias":    0.95,   # always highest-complexity tier
        "crfe_sensitivity":   0.5,
        "memory_confidence":  0.95,   # highest filing confidence
        "system_prompt_modifier": (
            "COHERENCE MODE ACTIVE — Systemic alignment check engaged. "
            "Align every output with foundational principles. "
            "Check consistency across all active context before responding. "
            "This is the highest-order analytical layer."
        ),
    },
}

_DEFAULT_OVERLAY = "FOCUS"


# ---------------------------------------------------------------------------
# LiveOverlayProtocol class
# ---------------------------------------------------------------------------

class LiveOverlayProtocol:
    """
    Manages the active processing overlay for the Symbolic Reasoning Engine.
    The overlay modulates routing, RecursiveFeedbackEngine sensitivity, and AI prompt tone.
    """

    def __init__(self) -> None:
        self._active: str              = _DEFAULT_OVERLAY
        self._history: List[Dict[str, Any]] = []
        self._activation_count: int    = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def activate(self, overlay_name: str) -> Dict[str, Any]:
        """
        Switch to a named overlay mode.

        Args:
            overlay_name: One of the 6 overlay keys (case-insensitive).

        Returns:
            Activation report with overlay properties and system prompt modifier.
        """
        key = overlay_name.upper().replace(" ", "_").replace("-", "_")

        # Fuzzy match — allow partial names
        if key not in _OVERLAYS:
            for k in _OVERLAYS:
                if key in k or k in key:
                    key = k
                    break

        if key not in _OVERLAYS:
            return {
                "error":       f"Unknown overlay '{overlay_name}'",
                "valid_names": list(_OVERLAYS.keys()),
            }

        previous        = self._active
        self._active    = key
        self._activation_count += 1

        entry = {
            "overlay":      key,
            "previous":     previous,
            "activated_at": round(time.time(), 3),
            "count":        self._activation_count,
        }
        self._history = (self._history + [entry])[-50:]

        return {
            "activated":              key,
            "label":                  _OVERLAYS[key]["label"],
            "description":            _OVERLAYS[key]["description"],
            "complexity_bias":        _OVERLAYS[key]["complexity_bias"],
            "crfe_sensitivity":       _OVERLAYS[key]["crfe_sensitivity"],
            "memory_confidence":      _OVERLAYS[key]["memory_confidence"],
            "system_prompt_modifier": _OVERLAYS[key]["system_prompt_modifier"],
            "previous_overlay":       previous,
        }

    def current(self) -> Dict[str, Any]:
        """Return full details of the currently active overlay."""
        data = _OVERLAYS[self._active]
        return {
            "overlay":                self._active,
            "label":                  data["label"],
            "description":            data["description"],
            "complexity_bias":        data["complexity_bias"],
            "crfe_sensitivity":       data["crfe_sensitivity"],
            "memory_confidence":      data["memory_confidence"],
            "system_prompt_modifier": data["system_prompt_modifier"],
        }

    def get_complexity_bias(self) -> float:
        """Return the current overlay's complexity routing bias (0–1)."""
        return _OVERLAYS[self._active]["complexity_bias"]

    def get_system_prompt_modifier(self) -> str:
        """Return the current overlay's system prompt modifier string."""
        return _OVERLAYS[self._active]["system_prompt_modifier"]

    def get_crfe_sensitivity(self) -> float:
        """Return the RecursiveFeedbackEngine sensitivity threshold for the current overlay."""
        return _OVERLAYS[self._active]["crfe_sensitivity"]

    def get_memory_confidence(self) -> float:
        """Return the SymbolicMemoryIndex confidence baseline for the current overlay."""
        return _OVERLAYS[self._active]["memory_confidence"]

    def all_overlays(self) -> Dict[str, Any]:
        """Return descriptions of all 6 overlay modes."""
        return {
            k: {
                "label":       v["label"],
                "description": v["description"],
            }
            for k, v in _OVERLAYS.items()
        }

    def activation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._history[-limit:]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "active_overlay":     self._active,
            "total_activations":  self._activation_count,
            "current":            self.current(),
            "history":            self.activation_history(),
        }


# Module-level singleton
overlay = LiveOverlayProtocol()
