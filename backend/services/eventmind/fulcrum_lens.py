"""
Fulcrum Lens
Reframes inputs by looking backward through implied causality
and projecting a forward outcome vector.

Two operations:
    backward_trace  — What likely caused or led to this input?
    forward_project — What outcome does this input imply or point toward?
"""
from __future__ import annotations

from typing import Dict, Any


# Causal back-trace patterns
_CAUSE_MAP = {
    "error":      "A prior system state or logic branch produced an unexpected result.",
    "slow":       "Resource saturation or unoptimised processing likely preceded this.",
    "fail":       "A dependency, condition, or constraint was not met upstream.",
    "confused":   "An ambiguous or incomplete information state preceded this moment.",
    "stuck":      "A decision loop or blocked pathway created this stasis.",
    "broken":     "A state change or external event disrupted a previously stable condition.",
    "lost":       "Navigation context was not preserved across a transition point.",
    "need":       "A gap between current state and desired state has been identified.",
    "want":       "A desired future state is not yet reachable from the current position.",
    "build":      "A vision of a new capability or system has reached activation threshold.",
    "create":     "Generative intent has been triggered by a recognised need or opportunity.",
    "help":       "A constraint or knowledge gap has been encountered that requires external input.",
}

# Forward projection patterns
_OUTCOME_MAP = {
    "build":      "A new system, module, or capability will emerge from this trajectory.",
    "create":     "An artifact — code, document, or design — will be produced.",
    "fix":        "System stability will be restored; the affected pathway will be cleared.",
    "learn":      "A knowledge node will be added to the memory lattice.",
    "deploy":     "The system will transition from development to an operational state.",
    "connect":    "A new integration bridge will be established between two nodes.",
    "analyze":    "A structured insight or pattern will surface from the data.",
    "understand": "A mental model will be updated or clarified.",
    "integrate":  "Two previously separate systems will function as a unified whole.",
    "optimize":   "Resource usage or response quality will improve measurably.",
    "test":       "A hypothesis about system behaviour will be confirmed or refuted.",
    "help":       "The constraint will be resolved; forward momentum will resume.",
}

_DEFAULT_CAUSE   = "An unmet need or unresolved state in a prior context generated this inquiry."
_DEFAULT_OUTCOME = "This input will initiate a processing sequence that moves the system toward a new stable state."


class ContextReframer:
    """
    Applies backward causality tracing and forward outcome projection
    to any input text.
    """

    def reframe(self, text: str) -> Dict[str, Any]:
        """
        Reframe the input through the Fulcrum Lens.

        Returns:
            {
                backward_trace: str,
                forward_projection: str,
                pivot_word: str | None,
                reframe_confidence: float
            }
        """
        words = text.lower().split()
        pivot_word = None
        backward = _DEFAULT_CAUSE
        forward = _DEFAULT_OUTCOME
        confidence = 0.4

        # Find the first matching pivot word
        for word in words:
            clean = word.strip(".,!?;:")
            if clean in _CAUSE_MAP:
                backward = _CAUSE_MAP[clean]
                pivot_word = clean
                confidence += 0.25
                break

        for word in words:
            clean = word.strip(".,!?;:")
            if clean in _OUTCOME_MAP:
                forward = _OUTCOME_MAP[clean]
                if pivot_word is None:
                    pivot_word = clean
                confidence += 0.25
                break

        confidence = round(min(confidence, 1.0), 4)

        return {
            "backward_trace": backward,
            "forward_projection": forward,
            "pivot_word": pivot_word,
            "reframe_confidence": confidence,
        }
