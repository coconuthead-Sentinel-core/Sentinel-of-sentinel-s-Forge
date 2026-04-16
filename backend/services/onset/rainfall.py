"""
Stream Ingester
Continuous real-time data ingestion layer.
New information is ingested as a stream and immediately indexed
into the KnowledgeGraph and MultiLayerMemoryStore.
"""
from __future__ import annotations

import re
import time
from typing import Dict, Any, List

from .spiderweb import knowledge_graph
from .spherical_memory import multi_layer_store


def _extract_concepts(text: str) -> List[str]:
    """Extract meaningful concept words from text (nouns, key terms)."""
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "about",
        "it", "this", "that", "these", "those", "i", "you", "we", "they",
        "he", "she", "and", "or", "but", "if", "then", "than", "so", "yet",
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [w for w in words if w not in stopwords]


class StreamIngester:
    """
    Manages real-time data ingestion into the Onset memory systems.
    """

    def __init__(self) -> None:
        self._stream_log: List[Dict[str, Any]] = []
        self._total_ingested: int = 0

    def ingest(self, text: str, source: str = "user_input", tags: List[str] = None) -> Dict[str, Any]:
        """
        Ingest a text stream into the KnowledgeGraph and MultiLayerMemoryStore.

        Args:
            text:    Raw text to ingest
            source:  Where this data came from
            tags:    Optional pre-assigned tags

        Returns:
            Ingestion report with node and memory stats
        """
        concepts = _extract_concepts(text)
        auto_tags = tags or []

        auto_tags.append(f"source:{source}")
        auto_tags.extend(concepts[:5])

        graph_stats = knowledge_graph.ingest(concepts)
        memory_entry = multi_layer_store.store(text, auto_tags)

        log_entry = {
            "timestamp": time.time(),
            "source": source,
            "concept_count": len(concepts),
            "top_concepts": concepts[:8],
            "tags": auto_tags,
        }
        self._stream_log.append(log_entry)
        if len(self._stream_log) > 200:
            self._stream_log = self._stream_log[-200:]

        self._total_ingested += 1

        return {
            "ingested": True,
            "concepts_extracted": len(concepts),
            "top_concepts": concepts[:8],
            "memory_entry_id": memory_entry["id"],
            "graph_nodes": graph_stats["node_count"],
            "total_ingested": self._total_ingested,
        }

    def recent_stream(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Return the most recent ingestion log entries."""
        return self._stream_log[-limit:]

    def stats(self) -> Dict[str, Any]:
        return {
            "total_ingested": self._total_ingested,
            "stream_log_size": len(self._stream_log),
        }


# Module-level singleton
stream_ingester = StreamIngester()
