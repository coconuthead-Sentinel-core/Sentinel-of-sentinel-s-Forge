"""
Chat Service
Thin coordination layer that delegates to CognitiveLensRouter.
Kept separate to preserve the public interface used by api.py.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ChatService:
    """
    Orchestrates the Cognitive Chat Pipeline via CognitiveLensRouter.

    Pipeline:
        1. Input validation
        2. Lens selection (profile parameter)
        3. AI generation + post-processing  (inside CognitiveLensRouter)
        4. Memory consolidation             (inside CognitiveLensRouter)
        5. Return structured response
    """

    def __init__(self, ai_adapter) -> None:
        from backend.services.cognitive_orchestrator import CognitiveLensRouter
        self._orchestrator = CognitiveLensRouter(ai_adapter)

    async def process_message(
        self,
        user_message: str,
        *,
        profile: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        context: str = "",  # kept for backward compat — ignored when orchestrator active
    ) -> Dict[str, Any]:
        """
        Process a user message through the full Sentinel cognitive pipeline.

        Args:
            user_message: The user's latest message text.
            profile: Cognitive lens profile. One of: adhd, autism, dyslexia, neurotypical.
            history: Prior conversation turns [{"role": "user"|"assistant", "content": "..."}].
            context: Legacy param — kept for API compatibility, not used.

        Returns:
            Azure OpenAI-compatible response dict, augmented with lens_metadata and latency_ms.
        """
        if not user_message or not user_message.strip():
            raise ValueError("user_message must be a non-empty string")

        return await self._orchestrator.process(
            user_message.strip(),
            profile=profile,
            history=history,
        )

    @staticmethod
    def available_profiles() -> List[Dict[str, Any]]:
        """Return metadata for all registered cognitive lens profiles."""
        from backend.services.cognitive_orchestrator import CognitiveLensRouter
        return CognitiveLensRouter.available_profiles()
