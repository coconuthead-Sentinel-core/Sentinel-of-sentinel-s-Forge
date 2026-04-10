"""
EventMind Engine
Orchestrates all EventMind components into a single processing pipeline.

Pipeline:
    Input → CorePulse → CoreSensor → TriangulationTelescope →
    FulcrumLens → ReturnVector → AI Generation → Output
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from .core_pulse import CorePulse
from .triangulation import TriangulationTelescope
from .fulcrum_lens import FulcrumLens
from .core_sensor import CoreSensor
from .return_vector import ReturnVector

logger = logging.getLogger(__name__)

# Module-level singletons (stateless per request, shared instances are safe)
_pulse       = CorePulse()
_telescope   = TriangulationTelescope()
_fulcrum     = FulcrumLens()
_sensor      = CoreSensor()
_return_vec  = ReturnVector()


class EventMindEngine:
    """
    Full EventMind processing pipeline.
    Wraps all five components and produces a complete analysis
    plus a system prompt for the AI generation layer.
    """

    def __init__(self, ai_adapter) -> None:
        self._adapter = ai_adapter

    async def process(
        self,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Run user_message through the complete EventMind pipeline.

        Returns the AI response augmented with full EventMind analysis.
        """
        t_start = time.perf_counter()

        # --- Stage 1: Core Pulse ---
        pulse = _pulse.measure(user_message)

        # --- Stage 2: Core Sensor ---
        sensor = _sensor.sense(user_message)

        # --- Stage 3: Triangulation Telescope ---
        triangulation = _telescope.analyze(user_message)

        # --- Stage 4: Fulcrum Lens ---
        fulcrum = _fulcrum.reframe(user_message)

        # --- Stage 5: Return Vector ---
        rv = _return_vec.compute(
            pulse_score=pulse["score"],
            triangulated_score=triangulation["triangulated_score"],
            urgency_level=sensor["urgency_level"],
            resonance_state=pulse["state"],
        )

        # --- Stage 6: If SILENT and no urgency, skip AI call ---
        if rv["delivery_mode"] == "SILENT":
            ai_response_text = pulse["hum"] or "~ The frequency is not aligned. Refocus your inquiry."
            raw_response = {
                "id": f"eventmind-silent-{int(time.time())}",
                "model": "eventmind-core",
                "created": int(time.time()),
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": ai_response_text},
                    "finish_reason": "stop",
                }],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            }
        else:
            # --- Stage 7: AI Generation with EventMind system prompt ---
            from backend.core.config import settings
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": rv["system_prompt_prefix"]}
            ]
            if history:
                for turn in history:
                    if turn.get("role") in ("user", "assistant") and turn.get("content"):
                        messages.append(turn)
            messages.append({"role": "user", "content": user_message})

            try:
                raw_response = await self._adapter.chat(
                    deployment=settings.AOAI_CHAT_DEPLOYMENT,
                    messages=messages,
                    temperature=0.75,
                    max_tokens=900,
                )
            except Exception as exc:
                logger.error("EventMind AI adapter error: %s", exc)
                raise

        # --- Stage 8: Assemble full EventMind report ---
        latency = round((time.perf_counter() - t_start) * 1000, 2)

        raw_response["eventmind_analysis"] = {
            "core_pulse": pulse,
            "core_sensor": sensor,
            "triangulation": triangulation,
            "fulcrum_lens": fulcrum,
            "return_vector": rv,
            "latency_ms": latency,
        }

        return raw_response

    @staticmethod
    def analyze_only(user_message: str) -> Dict[str, Any]:
        """
        Run the full EventMind analysis pipeline WITHOUT calling the AI.
        Useful for inspecting signal scores and reframes.
        """
        pulse        = _pulse.measure(user_message)
        sensor       = _sensor.sense(user_message)
        triangulation = _telescope.analyze(user_message)
        fulcrum      = _fulcrum.reframe(user_message)
        rv           = _return_vec.compute(
            pulse_score=pulse["score"],
            triangulated_score=triangulation["triangulated_score"],
            urgency_level=sensor["urgency_level"],
            resonance_state=pulse["state"],
        )
        return {
            "core_pulse": pulse,
            "core_sensor": sensor,
            "triangulation": triangulation,
            "fulcrum_lens": fulcrum,
            "return_vector": rv,
        }
