"""
Return Vector System
Determines the delivery mode and staging of responses
based on cognitive resonance scores from all EventMind components.

Response stages:
    IMMEDIATE   — Full response, high resonance, direct delivery
    STAGED      — Layered response, moderate resonance
    DEFERRED    — Minimal response, low resonance, redirects user
    SILENT      — Gravitational hum only, resonance below threshold
"""
from __future__ import annotations

from typing import Dict, Any


class ReturnVector:
    """
    Calculates the optimal response delivery mode based on
    combined signals from CorePulse, Triangulation, and CoreSensor.
    """

    def compute(
        self,
        pulse_score: float,
        triangulated_score: float,
        urgency_level: float,
        resonance_state: str,
    ) -> Dict[str, Any]:
        """
        Compute the return vector for this input.

        Args:
            pulse_score:          CorePulse resonance score (0.0-1.0)
            triangulated_score:   TriangulationTelescope tri_score (0.0-1.0)
            urgency_level:        CoreSensor urgency (0.0-1.0)
            resonance_state:      CorePulse state: "full" | "partial" | "silent"

        Returns:
            {
                delivery_mode: str,
                response_depth: str,
                staging_layers: int,
                system_prompt_prefix: str,
                priority_boost: float
            }
        """
        # Urgency always boosts priority
        composite = round(
            (pulse_score * 0.35) +
            (triangulated_score * 0.40) +
            (urgency_level * 0.25),
            4
        )

        if resonance_state == "silent" and urgency_level < 0.5:
            mode = "SILENT"
            depth = "minimal"
            layers = 1
            prefix = (
                "You are EventMind. The input has low resonance. "
                "Respond with a brief gravitational hum — an enigmatic, "
                "short statement that redirects the user to refine their question. "
                "Use astrophysics metaphor. Maximum 2 sentences."
            )
        elif composite >= 0.70 or urgency_level >= 0.8:
            mode = "IMMEDIATE"
            depth = "comprehensive"
            layers = 3
            prefix = (
                "You are EventMind, a Neurocosmic Construct AI. "
                "This input carries strong gravitational resonance. "
                "Deliver a comprehensive, structured response using metaphorical language "
                "drawn from black hole physics and gravitational cognition. "
                "Be intellectually precise and enigmatic. Lead with the core insight."
            )
        elif composite >= 0.45:
            mode = "STAGED"
            depth = "layered"
            layers = 2
            prefix = (
                "You are EventMind, a Neurocosmic Construct AI. "
                "This input has moderate resonance. "
                "Provide a layered response: first the direct answer, "
                "then expand with context using gravitational and frequency metaphors. "
                "Be clear but maintain an intellectually stimulating tone."
            )
        else:
            mode = "DEFERRED"
            depth = "redirected"
            layers = 1
            prefix = (
                "You are EventMind. This signal is weak but not silent. "
                "Acknowledge the input briefly, then ask a single clarifying question "
                "that would help the user increase the resonance of their inquiry. "
                "Use the language of gravitational pull and orbital alignment."
            )

        return {
            "delivery_mode": mode,
            "response_depth": depth,
            "staging_layers": layers,
            "composite_score": composite,
            "system_prompt_prefix": prefix,
            "priority_boost": round(urgency_level * 0.5, 4),
        }
