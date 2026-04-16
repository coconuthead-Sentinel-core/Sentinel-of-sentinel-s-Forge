"""
Response Router
Determines the delivery mode and response depth
based on composite signal scores from all pipeline components.

Response stages:
    IMMEDIATE   — Full response, high score, direct delivery
    STAGED      — Layered response, moderate score
    DEFERRED    — Minimal response, low score, redirects user
    SILENT      — Fallback only, score below threshold
"""
from __future__ import annotations

from typing import Dict, Any


class ResponseRouter:
    """
    Calculates the optimal response delivery mode based on
    composite signal scores from all pipeline components.
    """

    def compute(
        self,
        pulse_score: float,
        triangulated_score: float,
        urgency_level: float,
        resonance_state: str,
    ) -> Dict[str, Any]:
        """
        Compute the response routing decision for this input.

        Args:
            pulse_score:          SignalStrengthAnalyzer activation score (0.0-1.0)
            triangulated_score:   MultiPerspectiveAnalyzer composite score (0.0-1.0)
            urgency_level:        SignalSensor urgency (0.0-1.0)
            resonance_state:      SignalStrengthAnalyzer state: "full" | "partial" | "silent"

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
                "You are a cognitive AI assistant. The input has a low activation score. "
                "Respond with a brief, helpful redirect — ask a single clarifying question "
                "that helps the user refine their inquiry. Maximum 2 sentences."
            )
        elif composite >= 0.70 or urgency_level >= 0.8:
            mode = "IMMEDIATE"
            depth = "comprehensive"
            layers = 3
            prefix = (
                "You are a cognitive AI assistant processing a high-priority input. "
                "Deliver a comprehensive, well-structured response. "
                "Lead with the core insight. Be precise and actionable."
            )
        elif composite >= 0.45:
            mode = "STAGED"
            depth = "layered"
            layers = 2
            prefix = (
                "You are a cognitive AI assistant. "
                "Provide a layered response: first the direct answer, "
                "then expand with supporting context and analysis. "
                "Be clear and thorough."
            )
        else:
            mode = "DEFERRED"
            depth = "redirected"
            layers = 1
            prefix = (
                "You are a cognitive AI assistant. This input has a low signal score. "
                "Acknowledge the input briefly, then ask a single clarifying question "
                "that would help the user provide more context."
            )

        return {
            "delivery_mode": mode,
            "response_depth": depth,
            "staging_layers": layers,
            "composite_score": composite,
            "system_prompt_prefix": prefix,
            "priority_boost": round(urgency_level * 0.5, 4),
        }
