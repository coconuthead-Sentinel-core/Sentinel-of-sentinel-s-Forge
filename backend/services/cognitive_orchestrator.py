"""
Cognitive Orchestrator
Central routing layer that selects the appropriate cognitive lens,
assembles the AI prompt, calls the adapter, and post-processes the response.

Supported lens profiles:
  - adhd          ADHD Burst Mode
  - autism        Autism Precision Mode
  - dyslexia      Dyslexia Spatial Mode
  - dyscalculia   Dyscalculia Alternative Logic Mode
  - neurotypical  Baseline (default)
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from backend.core.config import settings
from backend.domain.models import Note
from backend.infrastructure.cosmos_repo import cosmos_repo
from backend.services import adhd_lens, autism_lens, dyslexia_lens, neurotypical_lens, dyscalculia_lens

logger = logging.getLogger(__name__)

# Lens registry: profile name → lens module
_LENS_REGISTRY = {
    "adhd":         adhd_lens,
    "autism":       autism_lens,
    "dyslexia":     dyslexia_lens,
    "dyscalculia":  dyscalculia_lens,
    "neurotypical": neurotypical_lens,
}

_DEFAULT_LENS = "neurotypical"


def _resolve_lens(profile: Optional[str]):
    """Return the lens module for the given profile, defaulting to neurotypical."""
    key = (profile or _DEFAULT_LENS).lower().strip()
    lens = _LENS_REGISTRY.get(key)
    if lens is None:
        logger.warning("Unknown cognitive profile '%s', falling back to neurotypical.", profile)
        lens = neurotypical_lens
    return lens


class CognitiveOrchestrator:
    """
    Routes each request through the correct cognitive lens and
    manages the full processing pipeline:

        Input → Lens Selection → Prompt Assembly →
        AI Generation → Post-Processing → Memory Consolidation → Output
    """

    def __init__(self, ai_adapter) -> None:
        self._adapter = ai_adapter

    async def process(
        self,
        user_message: str,
        *,
        profile: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Full cognitive pipeline.

        Args:
            user_message: The user's latest message.
            profile: Cognitive lens profile ('adhd', 'autism', 'dyslexia', 'neurotypical').
            history: Prior conversation turns as [{"role": ..., "content": ...}].

        Returns:
            dict with keys: id, model, created, choices, usage, lens_metadata
        """
        t_start = time.perf_counter()
        lens = _resolve_lens(profile)
        lens_meta = lens.metadata()

        # --- Prompt Assembly ---
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": lens.SYSTEM_PROMPT}
        ]
        if history:
            for turn in history:
                role = turn.get("role", "user")
                content = turn.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_message})

        # --- AI Generation ---
        params = dict(lens.GENERATION_PARAMS)
        deployment = settings.AOAI_CHAT_DEPLOYMENT

        logger.info(
            "CognitiveOrchestrator: lens=%s deployment=%s messages=%d",
            lens_meta["lens"], deployment, len(messages),
        )

        try:
            raw_response = await self._adapter.chat(
                deployment=deployment,
                messages=messages,
                temperature=params.get("temperature", 0.7),
                max_tokens=params.get("max_tokens"),
            )
        except Exception as exc:
            logger.error("AI adapter error in CognitiveOrchestrator: %s", exc)
            raise

        # --- Post-Processing ---
        choices = raw_response.get("choices", [])
        if choices:
            original_content = choices[0].get("message", {}).get("content", "")
            processed_content = lens.apply(original_content)
            # Mutate the response in-place so callers get the processed text
            raw_response["choices"][0]["message"]["content"] = processed_content

        # --- Memory Consolidation ---
        ai_text = processed_content if choices else ""
        if ai_text:
            try:
                note = Note(
                    text=f"User: {user_message}\nSentinel [{lens_meta['lens']}]: {ai_text}",
                    tag="chat-history",
                    metadata={
                        "type": "conversation",
                        "lens": lens_meta["lens"],
                        "latency_ms": round((time.perf_counter() - t_start) * 1000, 2),
                    },
                )
                await cosmos_repo.upsert_note(note)
            except Exception as exc:
                logger.warning("Memory consolidation failed (non-fatal): %s", exc)

        # Attach lens metadata to response for clients that want it
        raw_response["lens_metadata"] = lens_meta
        raw_response["latency_ms"] = round((time.perf_counter() - t_start) * 1000, 2)

        return raw_response

    @staticmethod
    def available_profiles() -> List[Dict[str, Any]]:
        """Return metadata for all registered lens profiles."""
        return [mod.metadata() for mod in _LENS_REGISTRY.values()]
