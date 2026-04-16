"""
Multi-Layer Memory Store
Three-tier cross-referenced memory storage.
Entries are promoted through tiers based on access frequency:

Layers:
    SURFACE   — Recent, immediately accessible entries
    MANTLE    — Pattern-matched, cross-referenced entries
    CORE      — High-confidence long-term entries
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional


class MemoryEntry:
    def __init__(self, content: str, tags: List[str], layer: str = "SURFACE") -> None:
        self.id = str(uuid.uuid4())[:8]
        self.content = content
        self.tags = tags
        self.layer = layer
        self.created_at = time.time()
        self.access_count = 0
        self.confidence: float = 0.5

    def access(self) -> None:
        self.access_count += 1
        if self.access_count >= 10 and self.layer == "MANTLE":
            self.layer = "CORE"
            self.confidence = min(self.confidence + 0.1, 1.0)
        elif self.access_count >= 3 and self.layer == "SURFACE":
            self.layer = "MANTLE"
            self.confidence = min(self.confidence + 0.05, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content[:200],
            "tags": self.tags,
            "layer": self.layer,
            "access_count": self.access_count,
            "confidence": self.confidence,
            "age_seconds": round(time.time() - self.created_at, 1),
        }


class MultiLayerMemoryStore:
    """
    Three-tier memory system with cross-referencing via tags.
    """

    def __init__(self, capacity: int = 1000) -> None:
        self._entries: Dict[str, MemoryEntry] = {}
        self._tag_index: Dict[str, List[str]] = {}  # tag → [entry_ids]
        self._capacity = capacity

    def store(self, content: str, tags: List[str]) -> Dict[str, Any]:
        """Store a new memory entry and index it by tags."""
        if len(self._entries) >= self._capacity:
            self._evict()

        entry = MemoryEntry(content, tags)
        self._entries[entry.id] = entry

        for tag in tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = []
            self._tag_index[tag].append(entry.id)

        return entry.to_dict()

    def retrieve_by_tag(self, tag: str, layer: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all entries matching a tag, optionally filtered by layer."""
        ids = self._tag_index.get(tag, [])
        results = []
        for entry_id in ids:
            if entry_id in self._entries:
                entry = self._entries[entry_id]
                if layer is None or entry.layer == layer:
                    entry.access()
                    results.append(entry.to_dict())
        return sorted(results, key=lambda e: e["confidence"], reverse=True)

    def cross_reference(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Find entries that match ALL provided tags (intersection)."""
        if not tags:
            return []
        candidate_sets = [set(self._tag_index.get(t, [])) for t in tags]
        common_ids = candidate_sets[0].intersection(*candidate_sets[1:])
        results = []
        for entry_id in common_ids:
            if entry_id in self._entries:
                entry = self._entries[entry_id]
                entry.access()
                results.append(entry.to_dict())
        return results

    def layer_snapshot(self) -> Dict[str, Any]:
        """Return counts and top entries per layer."""
        layers: Dict[str, List] = {"SURFACE": [], "MANTLE": [], "CORE": []}
        for entry in self._entries.values():
            layers[entry.layer].append(entry.to_dict())

        return {
            layer: {
                "count": len(entries),
                "top": sorted(entries, key=lambda e: e["confidence"], reverse=True)[:5],
            }
            for layer, entries in layers.items()
        }

    def _evict(self) -> None:
        """Evict lowest-confidence SURFACE entries to make room."""
        surface = [e for e in self._entries.values() if e.layer == "SURFACE"]
        surface.sort(key=lambda e: e.confidence)
        for entry in surface[:self._capacity // 10]:
            for tag in entry.tags:
                if tag in self._tag_index:
                    self._tag_index[tag] = [i for i in self._tag_index[tag] if i != entry.id]
            del self._entries[entry.id]


# Module-level singleton
multi_layer_store = MultiLayerMemoryStore()
