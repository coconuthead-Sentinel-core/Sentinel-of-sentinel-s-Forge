"""
Live Overlay Protocol
Six named cognitive overlay nodes that modulate how VoidLogic
processes and responds to input. Each overlay shifts the CNO
routing priority, CRFE sensitivity, and AI system prompt tone.

Overlay Nodes (from the Quantum Cognitive System diagram):
    INITIATIVE_NODE    — Sets task focus, high-priority routing
    REFLECTIVE_MIRBOR  — Recursive context recalibration (Mirror Pool)
    GEOMETRIC_HARMONIOS — Logic-metaphor spatial alignment
    COO_X_MODE         — Codified Optimization Overlay, streamlines reasoning
    NEKUM_AFTIRRAD     — Dual-flow ambiguity + divergent synthesis node
    METATRON_CORE      — Systemic resonance checker, alignment with core principles

Only one overlay is active at a time. The overlay modulates:
    • The VoidLogic engine's system prompt prefix
    • The CNO complexity routing bias
    • The CRFE sensitivity thresholds
    • The A1 filing confidence baseline
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Overlay definitions
# ---------------------------------------------------------------------------

_OVERLAYS: Dict[str, Dict[str, Any]] = {
    "INITIATIVE_NODE": {
        "label":       "Initiative Node",
        "description": "Sets task focus. Routes all payloads to high-complexity Icosahedral tier. Maximises analytical depth.",
        "complexity_bias":   0.85,   # pushes routing toward Icosahedral
        "crfe_sensitivity":  0.6,    # standard CRFE thresholds
        "a1_confidence":     0.85,   # high filing confidence
        "system_prompt_modifier": (
            "⚙️ INITIATIVE NODE ACTIVE — Task focus locked. "
            "Operate with maximum analytical clarity. "
            "Prioritise structured, actionable output."
        ),
    },
    "REFLECTIVE_MIRBOR": {
        "label":       "Reflective Mirbor (Mirror Pool)",
        "description": "Recursive context recalibration. Surfaces contradictions, revisits prior assumptions, deepens self-reference.",
        "complexity_bias":   0.65,
        "crfe_sensitivity":  0.4,    # lower threshold — catches more recursion
        "a1_confidence":     0.75,
        "system_prompt_modifier": (
            "🪞 REFLECTIVE MIRBOR ACTIVE — Mirror Pool engaged. "
            "Revisit assumptions. Surface contradictions. "
            "Recalibrate against prior context before responding."
        ),
    },
    "GEOMETRIC_HARMONIOS": {
        "label":       "Geometric Harmonios",
        "description": "Aligns logic with spatial/metaphorical structure. Bridges symbolic and rational domains.",
        "complexity_bias":   0.55,
        "crfe_sensitivity":  0.5,
        "a1_confidence":     0.80,
        "system_prompt_modifier": (
            "🔷 GEOMETRIC HARMONIOS ACTIVE — Spatial logic alignment engaged. "
            "Ground abstract concepts in geometric or metaphorical structure. "
            "Bridge the symbolic and the rational in every response."
        ),
    },
    "COO_X_MODE": {
        "label":       "COO-X Mode (Codified Optimization Overlay)",
        "description": "Streamlines reasoning. Eliminates redundancy. Optimises output for clarity and speed.",
        "complexity_bias":   0.45,   # routes toward faster Octahedral tier
        "crfe_sensitivity":  0.7,    # strict — only strong signals matter
        "a1_confidence":     0.90,
        "system_prompt_modifier": (
            "⚡ COO-X MODE ACTIVE — Codified Optimization Overlay engaged. "
            "Be precise. Eliminate redundancy. "
            "Every word earns its place. Optimise for clarity above all."
        ),
    },
    "NEKUM_AFTIRRAD": {
        "label":       "Nekum Aftirrad (Dual-Flow Divergent Synthesis)",
        "description": "Holds two conflicting ideas simultaneously. Synthesises divergent paths. For paradox, ambiguity, and creative leaps.",
        "complexity_bias":   0.75,
        "crfe_sensitivity":  0.3,    # very sensitive — detects weak paradoxes
        "a1_confidence":     0.65,   # lower confidence — divergent terrain
        "system_prompt_modifier": (
            "🌀 NEKUM AFTIRRAD ACTIVE — Dual-flow synthesis engaged. "
            "Hold contradictions. Do not collapse ambiguity prematurely. "
            "Synthesise divergent paths into emergent understanding."
        ),
    },
    "METATRON_CORE": {
        "label":       "Metatron Core (Systemic Resonance Checker)",
        "description": "Checks alignment with core principles. Highest-tier oversight. Ensures all outputs resonate with foundational values.",
        "complexity_bias":   0.95,   # always Icosahedral
        "crfe_sensitivity":  0.5,
        "a1_confidence":     0.95,   # highest filing confidence
        "system_prompt_modifier": (
            "💠 METATRON CORE ACTIVE — Systemic resonance engaged. "
            "Align every output with foundational principles. "
            "Check coherence across all active modules before responding. "
            "This is the highest-order cognitive layer."
        ),
    },
}

_DEFAULT_OVERLAY = "INITIATIVE_NODE"


# ---------------------------------------------------------------------------
# LiveOverlayProtocol class
# ---------------------------------------------------------------------------

class LiveOverlayProtocol:
    """
    Manages the active cognitive overlay node for VoidLogic.
    The overlay modulates routing, CRFE sensitivity, and AI prompt tone.
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
        Switch to a named overlay node.

        Args:
            overlay_name: One of the 6 overlay node keys (case-insensitive).

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
            "overlay":    key,
            "previous":   previous,
            "activated_at": round(time.time(), 3),
            "count":      self._activation_count,
        }
        self._history = (self._history + [entry])[-50:]

        return {
            "activated":              key,
            "label":                  _OVERLAYS[key]["label"],
            "description":            _OVERLAYS[key]["description"],
            "complexity_bias":        _OVERLAYS[key]["complexity_bias"],
            "crfe_sensitivity":       _OVERLAYS[key]["crfe_sensitivity"],
            "a1_confidence_baseline": _OVERLAYS[key]["a1_confidence"],
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
            "a1_confidence_baseline": data["a1_confidence"],
            "system_prompt_modifier": data["system_prompt_modifier"],
        }

    def get_complexity_bias(self) -> float:
        """Return the current overlay's complexity routing bias (0–1)."""
        return _OVERLAYS[self._active]["complexity_bias"]

    def get_system_prompt_modifier(self) -> str:
        """Return the current overlay's system prompt modifier string."""
        return _OVERLAYS[self._active]["system_prompt_modifier"]

    def get_crfe_sensitivity(self) -> float:
        """Return the CRFE sensitivity threshold for the current overlay."""
        return _OVERLAYS[self._active]["crfe_sensitivity"]

    def get_a1_confidence(self) -> float:
        """Return the A1 filing confidence baseline for the current overlay."""
        return _OVERLAYS[self._active]["a1_confidence"]

    def all_overlays(self) -> Dict[str, Any]:
        """Return descriptions of all 6 overlay nodes."""
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
