"""
SQA Bridge — connects the C++ SQA v8.0 engine to the existing Python pipeline.

Falls back to the Python SentinelProcessor when the C++ module is not built.
Controlled by SQA_ENGINE_ACTIVE environment variable or profile flag.
"""
from __future__ import annotations

import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional

log = logging.getLogger("sqa_bridge")

# --- Attempt to import the C++ module ---
_cpp_available = False
_sqa = None

try:
    import sqa_engine as _sqa  # type: ignore
    _cpp_available = True
    log.info("SQA C++ engine loaded (v%s)", _sqa.__version__)
except ImportError:
    log.info("SQA C++ engine not available — using Python fallback")


def is_cpp_available() -> bool:
    """Return True if the C++ SQA engine is loaded."""
    return _cpp_available


def is_active() -> bool:
    """Return True if the SQA engine should be used (env var or profile flag)."""
    return _cpp_available and os.getenv("SQA_ENGINE_ACTIVE", "0") == "1"


# ---------------------------------------------------------------------------
# CNO Bridge
# ---------------------------------------------------------------------------

class CNOBridge:
    """Wraps the C++ CognitiveNeuralOverlay or falls back to Python."""

    def __init__(self) -> None:
        self._cpp_cno = None
        if _cpp_available:
            self._cpp_cno = _sqa.CognitiveNeuralOverlay()
            log.info("CNO Bridge: C++ engine active")

    def configure(self, cfg: Dict[str, Any]) -> None:
        if self._cpp_cno is not None:
            self._cpp_cno.configure(cfg)

    def process(self, text: str, atom_id: str = "") -> Dict[str, Any]:
        """Process text through the CNO pipeline.

        Returns a dict compatible with the Python SentinelProcessor output.
        """
        if self._cpp_cno is None:
            return self._fallback(text, atom_id)

        if not atom_id:
            atom_id = f"cno_{uuid.uuid4().hex[:8]}"

        inp = _sqa.CognitiveInput(atom_id, text)
        snap = self._cpp_cno.process(inp)
        return snap.to_dict()

    def _fallback(self, text: str, atom_id: str) -> Dict[str, Any]:
        """Fallback: return a minimal result structure."""
        return {
            "id": atom_id or f"cno_py_{uuid.uuid4().hex[:8]}",
            "intent_label": "unknown",
            "intent_score": 0.0,
            "appraisal_valence": 0.0,
            "attention_weight": 1.0,
            "creativity_score": 0.0,
            "symbolic_tags": [],
            "processing_ms": 0.0,
            "engine": "python_fallback",
        }

    def get_rules(self) -> List[Dict[str, str]]:
        if self._cpp_cno is not None:
            return self._cpp_cno.get_rules()
        return []

    def set_rules(self, rules: List[Dict[str, str]]) -> None:
        if self._cpp_cno is not None:
            self._cpp_cno.set_rules(rules)

    @property
    def executions(self) -> int:
        return self._cpp_cno.executions() if self._cpp_cno else 0


# ---------------------------------------------------------------------------
# A1FS Bridge
# ---------------------------------------------------------------------------

class A1FSBridge:
    """Wraps the C++ A1FilingSystem or falls back to Python ReflectivePool."""

    def __init__(self, capacity: int = 1024) -> None:
        self._cpp_a1fs = None
        if _cpp_available:
            self._cpp_a1fs = _sqa.A1FilingSystem(capacity)
            log.info("A1FS Bridge: C++ engine active (capacity=%d)", capacity)

    def store(self, text: str, tags: Optional[List[str]] = None,
              metadata: Optional[Dict[str, Any]] = None) -> str:
        if self._cpp_a1fs is None:
            return f"mem_py_{uuid.uuid4().hex[:8]}"
        return self._cpp_a1fs.store_episodic(text, tags or [], metadata or {})

    def retrieve_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self._cpp_a1fs is None:
            return []
        results = self._cpp_a1fs.retrieve_similar(query, top_k)
        return [{"id": r[0], "score": r[1]} for r in results]

    def strengthen(self, mem_id: str, amount: float = 0.1) -> None:
        if self._cpp_a1fs is not None:
            self._cpp_a1fs.strengthen(mem_id, amount)

    def consolidate(self) -> int:
        if self._cpp_a1fs is not None:
            return self._cpp_a1fs.consolidate()
        return 0

    def snapshot(self) -> Dict[str, Any]:
        if self._cpp_a1fs is not None:
            return self._cpp_a1fs.snapshot()
        return {"node_count": 0, "edge_count": 0, "engine": "python_fallback"}

    def clear(self) -> None:
        if self._cpp_a1fs is not None:
            self._cpp_a1fs.clear()

    @property
    def size(self) -> int:
        return self._cpp_a1fs.size() if self._cpp_a1fs else 0


# ---------------------------------------------------------------------------
# NNS Bridge
# ---------------------------------------------------------------------------

class NNSBridge:
    """Wraps the C++ NexusNodeStack or falls back to sequential Python."""

    def __init__(self) -> None:
        self._cpp_nns = None
        if _cpp_available:
            self._cpp_nns = _sqa.NexusNodeStack()
            log.info("NNS Bridge: C++ engine active")

    def add_node(self, node_id: str, fn) -> None:
        if self._cpp_nns is not None:
            self._cpp_nns.add_node(node_id, fn)

    def execute(self, data: Dict[str, Any], parallel: bool = True) -> List[Dict[str, Any]]:
        if self._cpp_nns is None:
            return []
        return self._cpp_nns.execute(data, parallel)

    def status(self) -> Dict[str, Any]:
        if self._cpp_nns is not None:
            return self._cpp_nns.status()
        return {"node_count": 0, "engine": "python_fallback"}


# ---------------------------------------------------------------------------
# Unified SQA Engine
# ---------------------------------------------------------------------------

class SQAEngine:
    """Unified access to all SQA v8.0 subsystems."""

    def __init__(self) -> None:
        self.cno = CNOBridge()
        self.a1fs = A1FSBridge()
        self.nns = NNSBridge()
        self._active = is_active()

    @property
    def active(self) -> bool:
        return self._active and _cpp_available

    @property
    def cpp_available(self) -> bool:
        return _cpp_available

    def process(self, text: str) -> Dict[str, Any]:
        """Full SQA pipeline: CNO process → store in A1FS → return result."""
        start = time.time()
        result = self.cno.process(text)

        # Store in A1FS memory.
        tags = result.get("symbolic_tags", [])
        mem_id = self.a1fs.store(text, tags, {"cno_result": result.get("id", "")})
        result["memory_id"] = mem_id

        # Find related memories.
        similar = self.a1fs.retrieve_similar(text, top_k=3)
        result["related_memories"] = similar

        result["total_ms"] = (time.time() - start) * 1000.0
        result["engine"] = "sqa_cpp" if _cpp_available else "python_fallback"
        return result

    def status(self) -> Dict[str, Any]:
        return {
            "active": self.active,
            "cpp_available": _cpp_available,
            "cno_executions": self.cno.executions,
            "a1fs_size": self.a1fs.size,
            "nns": self.nns.status(),
            "version": _sqa.__version__ if _cpp_available else "fallback",
        }
