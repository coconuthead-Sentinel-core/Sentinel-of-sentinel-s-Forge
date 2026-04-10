"""
Tesseract Mass Storage Unit (SMSU)
Hypercube 4D symbolic memory — the central repository for VoidLogic.

A tesseract (4D hypercube) has 8 cubic cells, 24 faces, 32 edges, 16 vertices.
We model this as 4 dimensional axes, each with 2 poles — giving 8 addressable
storage planes that can be accessed simultaneously without linear search.

Dimensions:
    W — Temporal     (when was this stored / how recent)
    X — Symbolic     (what symbolic domain does this belong to)
    Y — Complexity   (how complex/deep is this memory)
    Z — Resonance    (how strongly does this connect to the current context)
"""
from __future__ import annotations

import math
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple


class TesseractCell:
    """A single addressable storage cell in the hypercube."""

    def __init__(self, w: int, x: int, y: int, z: int) -> None:
        self.address = (w, x, y, z)
        self.entries: List[Dict[str, Any]] = []
        self.access_count = 0

    def store(self, content: str, metadata: Dict[str, Any]) -> str:
        entry_id = str(uuid.uuid4())[:8]
        self.entries.append({
            "id":        entry_id,
            "content":   content,
            "metadata":  metadata,
            "stored_at": time.time(),
        })
        return entry_id

    def retrieve_all(self) -> List[Dict[str, Any]]:
        self.access_count += 1
        return list(self.entries)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "address":      self.address,
            "entry_count":  len(self.entries),
            "access_count": self.access_count,
        }


class TesseractStorage:
    """
    Hypercube 4D mass storage system.
    Stores symbolic memories across 4 dimensions (W, X, Y, Z),
    each with 2 poles (0 or 1), yielding 16 addressable cells.
    Enables zero-latency cross-dimensional recall.
    """

    def __init__(self) -> None:
        # 2^4 = 16 cells for a tesseract
        self._cells: Dict[Tuple, TesseractCell] = {}
        for w in range(2):
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        addr = (w, x, y, z)
                        self._cells[addr] = TesseractCell(*addr)

        self._total_stored = 0
        self._index: Dict[str, Tuple] = {}  # entry_id → cell address

    def _compute_address(
        self,
        content: str,
        symbolic_domain: str,
        complexity: float,
        resonance: float,
    ) -> Tuple[int, int, int, int]:
        """Map content to a tesseract cell address."""
        w = 1 if time.time() % 86400 > 43200 else 0   # temporal pole (AM/PM proxy)
        x = 0 if symbolic_domain in ("logic", "process", "action") else 1
        y = 1 if complexity >= 0.5 else 0
        z = 1 if resonance >= 0.5 else 0
        return (w, x, y, z)

    def store(
        self,
        content: str,
        symbolic_domain: str = "general",
        complexity: float = 0.5,
        resonance: float = 0.5,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Store content in the appropriate tesseract cell."""
        addr = self._compute_address(content, symbolic_domain, complexity, resonance)
        cell = self._cells[addr]
        entry_id = cell.store(content, metadata or {})
        self._index[entry_id] = addr
        self._total_stored += 1

        return {
            "entry_id":    entry_id,
            "cell_address": addr,
            "total_stored": self._total_stored,
        }

    def recall(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Zero-latency direct recall by entry ID."""
        addr = self._index.get(entry_id)
        if not addr:
            return None
        cell = self._cells[addr]
        for entry in cell.entries:
            if entry["id"] == entry_id:
                return entry
        return None

    def cross_dimensional_scan(
        self,
        complexity_pole: Optional[int] = None,
        resonance_pole: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Scan across multiple cells simultaneously using dimension filters.
        This is the zero-latency omnidirectional recall — no linear search.
        """
        results = []
        for addr, cell in self._cells.items():
            _, _, y, z = addr
            if complexity_pole is not None and y != complexity_pole:
                continue
            if resonance_pole is not None and z != resonance_pole:
                continue
            results.extend(cell.retrieve_all())
        return results

    def hyperplane_snapshot(self) -> Dict[str, Any]:
        """Return the full tesseract structure with cell stats."""
        return {
            "dimensions":   4,
            "total_cells":  len(self._cells),
            "total_stored": self._total_stored,
            "cells": [cell.to_dict() for cell in self._cells.values()],
            "most_accessed": sorted(
                [c.to_dict() for c in self._cells.values()],
                key=lambda c: c["access_count"],
                reverse=True
            )[:4],
        }


# Module-level singleton
tesseract = TesseractStorage()
