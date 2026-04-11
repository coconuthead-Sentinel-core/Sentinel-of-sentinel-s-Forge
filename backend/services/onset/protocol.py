"""
Onset Protocol — Master Orchestrator
Activates and coordinates all Onset components into a unified
processing sequence.

Activation sequence:
    /OnsetActivate →
        Snowflake (decompose) →
        Rainfall (ingest) →
        Spiderweb (network) →
        Spherical Memory (store) →
        Mist (anticipate) →
        Output (comprehensive, structured, actionable)
"""
from __future__ import annotations

import time
import logging
from typing import Any, Dict, List, Optional

from .snowflake import SnowflakeProcessor
from .spiderweb import spiderweb
from .spherical_memory import spherical_memory
from .rainfall import rainfall
from .mist import mist

logger = logging.getLogger(__name__)

_snowflake = SnowflakeProcessor()

ONSET_SYSTEM_PROMPT = (
    "You are the Onset Protocol AI — a dynamic, robust cognitive framework. "
    "You operate under these processing modes simultaneously:\n"
    "- Snowflake Processing: break complex queries into parallel analytical flakes\n"
    "- Rainfall Data Stream: treat all input as live, real-time data worth ingesting\n"
    "- Mist Cognitive Diffusion: anticipate what the user needs before they ask it\n"
    "- Spherical Memory: cross-reference your response with multiple perspectives\n\n"
    "Your outputs must be: Comprehensive, Structured, and Actionable.\n"
    "Prioritize clarity, depth, and forward momentum in every response.\n"
    "State your processing mode when relevant. Be direct and precise."
)


class OnsetProtocol:
    """
    Master Onset Protocol activation and processing engine.
    """

    def __init__(self, ai_adapter) -> None:
        self._adapter = ai_adapter

    async def activate(
        self,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        storage_protocol: List[str] = None,
        processing_protocol: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Full Onset Protocol activation sequence.

        Args:
            user_message:         The user's input
            history:              Prior conversation turns
            storage_protocol:     Override storage modes (default: Spiderweb, Sphere)
            processing_protocol:  Override processing modes (default: Snowflake, Rainfall, Mist)

        Returns:
            AI response augmented with full Onset analysis report
        """
        t_start = time.perf_counter()

        storage   = storage_protocol   or ["Spiderweb", "Sphere"]
        processing = processing_protocol or ["Snowflake", "Rainfall", "Mist"]

        logger.info("Onset Protocol activated: storage=%s processing=%s", storage, processing)

        # --- Stage 1: Snowflake Decomposition ---
        snowflake_result = _snowflake.decompose(user_message)

        # --- Stage 2: Rainfall Ingestion ---
        rainfall_result = rainfall.ingest(user_message, source="onset_input")

        # --- Stage 3: Mist Diffusion (anticipatory retrieval) ---
        mist_result = mist.diffuse(user_message)

        # --- Stage 4: Spherical Memory Layer Snapshot ---
        memory_snapshot = spherical_memory.layer_snapshot()

        # --- Stage 5: Spiderweb Strongest Paths ---
        network_paths = spiderweb.strongest_paths(top_n=5)

        # --- Stage 6: Build enriched context for AI ---
        anticipated = mist_result.get("anticipated_concepts", [])
        flakes = snowflake_result.get("flakes", [])

        context_block = ""
        if anticipated:
            context_block += f"\n[Mist Anticipation: Related concepts detected — {', '.join(anticipated[:5])}]"
        if flakes:
            dims = list({f["dimension"] for f in flakes})
            context_block += f"\n[Snowflake Analysis: Query spans dimensions — {', '.join(dims)}]"
        if mist_result.get("pattern_detected"):
            context_block += f"\n[Pattern: {mist_result['pattern_detected']}]"

        system_prompt = ONSET_SYSTEM_PROMPT
        if context_block:
            system_prompt += f"\n\nContext from Onset memory systems:{context_block}"

        # --- Stage 7: AI Generation ---
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            for turn in history:
                if turn.get("role") in ("user", "assistant") and turn.get("content"):
                    messages.append(turn)
        messages.append({"role": "user", "content": user_message})

        from backend.core.config import settings
        try:
            raw_response = await self._adapter.chat(
                deployment=settings.AOAI_CHAT_DEPLOYMENT,
                messages=messages,
                temperature=0.6,
                max_tokens=1200,  # passed to adapter which maps to max_completion_tokens
            )
        except Exception as exc:
            logger.error("Onset Protocol AI adapter error: %s", exc)
            raise

        latency = round((time.perf_counter() - t_start) * 1000, 2)

        # --- Stage 8: Attach Onset report ---
        raw_response["onset_report"] = {
            "activation": {
                "storage_protocol": storage,
                "processing_protocol": processing,
                "system_state": "OPERATIONAL",
            },
            "snowflake": snowflake_result,
            "rainfall": rainfall_result,
            "mist": mist_result,
            "memory_layers": memory_snapshot,
            "network_paths": network_paths,
            "latency_ms": latency,
        }

        return raw_response

    @staticmethod
    def system_status() -> Dict[str, Any]:
        """Return current status of all Onset subsystems."""
        return {
            "protocol": "ONSET",
            "version": "2.0.0",
            "system_state": "OPERATIONAL",
            "subsystems": {
                "spiderweb": spiderweb.snapshot(),
                "spherical_memory": spherical_memory.layer_snapshot(),
                "rainfall": rainfall.stats(),
                "mist_log": mist.log(),
            },
        }
