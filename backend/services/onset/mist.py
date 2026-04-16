"""
Predictive Retriever
Background anticipatory retrieval system.
Analyzes patterns in user input and proactively surfaces
related concepts before they are explicitly requested.
"""
from __future__ import annotations

import re
import time
from typing import Dict, Any, List

from .spiderweb import knowledge_graph
from .spherical_memory import multi_layer_store


class PredictiveRetriever:
    """
    Anticipatory retrieval engine — surfaces related context
    based on current input without being explicitly asked.
    """

    def __init__(self) -> None:
        self._recent_queries: List[str] = []
        self._retrieval_log: List[Dict[str, Any]] = []

    def diffuse(self, current_input: str) -> Dict[str, Any]:
        """
        Analyze current input and surface proactively relevant context
        from KnowledgeGraph and MultiLayerMemoryStore.

        Returns:
            {
                anticipated_concepts: [str],
                related_memories: [...],
                strongest_paths: [...],
                pattern_detected: str | None,
                retrieval_confidence: float
            }
        """
        self._recent_queries.append(current_input)
        if len(self._recent_queries) > 20:
            self._recent_queries = self._recent_queries[-20:]

        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', current_input.lower()))

        anticipated: List[str] = []
        for word in words:
            result = knowledge_graph.retrieve(word, depth=2)
            if result.get("found"):
                neighbours = result.get("neighbours", {})
                anticipated.extend(list(neighbours.keys())[:3])

        anticipated = list(set(anticipated) - words)[:8]

        related_memories = []
        for concept in list(words)[:5]:
            memories = multi_layer_store.retrieve_by_tag(concept)
            related_memories.extend(memories[:2])

        seen_ids = set()
        unique_memories = []
        for m in related_memories:
            if m["id"] not in seen_ids:
                seen_ids.add(m["id"])
                unique_memories.append(m)

        pattern = self._detect_pattern()

        confidence = round(min(
            (len(anticipated) * 0.1) + (len(unique_memories) * 0.15),
            1.0
        ), 4)

        result = {
            "anticipated_concepts": anticipated,
            "related_memories": unique_memories[:5],
            "strongest_paths": knowledge_graph.strongest_paths(5),
            "pattern_detected": pattern,
            "retrieval_confidence": confidence,
        }

        self._retrieval_log.append({
            "timestamp": time.time(),
            "input_preview": current_input[:80],
            "anticipated_count": len(anticipated),
            "confidence": confidence,
        })

        return result

    def _detect_pattern(self) -> str | None:
        """Detect if there is a recurring theme in recent queries."""
        if len(self._recent_queries) < 3:
            return None

        all_words = " ".join(self._recent_queries[-5:]).lower()
        word_freq: Dict[str, int] = {}
        for word in re.findall(r'\b[a-zA-Z]{4,}\b', all_words):
            word_freq[word] = word_freq.get(word, 0) + 1

        patterns = [w for w, c in word_freq.items() if c >= 3]
        if patterns:
            return f"Recurring focus: {', '.join(patterns[:3])}"
        return None

    def log(self) -> List[Dict[str, Any]]:
        return self._retrieval_log[-10:]


# Module-level singleton
predictive_retriever = PredictiveRetriever()
