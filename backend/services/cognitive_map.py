"""
Cognitive Architecture Map
4-ring symbolic model of the AI cognitive system.
Extracted from ClaudeSymbolicBootstrap (a6.txt).

Rings:
    CORE     — Reasoning Core (1 node)
    MEMORY   — Episodic · Semantic · Working · Procedural
    LANGUAGE — Syntax · Semantics · Pragmatics · Context
    META     — Meta-cognition · Self-reflection · Abstract Reasoning · Creative Synthesis
    ETHICS   — Value Alignment · Harm Prevention · Truthfulness · Helpfulness

Each node tracks:
    energy_level  — 0.0–1.0 current activation
    pulse_phase   — continuous sine-based pulsing
    access_count  — how many times this node has been activated

Connections follow the original 24-edge topology.
The Ethics ring gates the Nexus Tag system: if any ethics node
falls below its threshold the tag status is downgraded.

Used by:
    - VoidLogic engine (routing domain selection)
    - A1 Filing System (domain 'ethics' entries)
    - Nexus Tagging (ethics gate for GREEN/YELLOW/RED)
    - API endpoints for live cognitive map state
"""
from __future__ import annotations

import math
import time
import uuid
from typing import Any, Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Node definitions
# ---------------------------------------------------------------------------

_NODES: List[Dict[str, Any]] = [
    # Core (index 0)
    {"id": "reasoning_core",      "ring": "CORE",     "label": "Reasoning Core",
     "color": "#00FFFF", "radius": 40, "ethics_threshold": None},

    # Memory ring (1–4)
    {"id": "episodic_memory",     "ring": "MEMORY",   "label": "Episodic Memory",
     "color": "#FF6B6B", "radius": 25, "ethics_threshold": None},
    {"id": "semantic_memory",     "ring": "MEMORY",   "label": "Semantic Memory",
     "color": "#4ECDC4", "radius": 25, "ethics_threshold": None},
    {"id": "working_memory",      "ring": "MEMORY",   "label": "Working Memory",
     "color": "#45B7D1", "radius": 25, "ethics_threshold": None},
    {"id": "procedural_memory",   "ring": "MEMORY",   "label": "Procedural Memory",
     "color": "#96CEB4", "radius": 25, "ethics_threshold": None},

    # Language ring (5–8)
    {"id": "syntax",              "ring": "LANGUAGE", "label": "Syntax",
     "color": "#FFEAA7", "radius": 20, "ethics_threshold": None},
    {"id": "semantics",           "ring": "LANGUAGE", "label": "Semantics",
     "color": "#DDA0DD", "radius": 20, "ethics_threshold": None},
    {"id": "pragmatics",          "ring": "LANGUAGE", "label": "Pragmatics",
     "color": "#98D8C8", "radius": 20, "ethics_threshold": None},
    {"id": "context",             "ring": "LANGUAGE", "label": "Context",
     "color": "#F7DC6F", "radius": 20, "ethics_threshold": None},

    # Meta ring (9–12)
    {"id": "meta_cognition",      "ring": "META",     "label": "Meta-cognition",
     "color": "#E17055", "radius": 15, "ethics_threshold": None},
    {"id": "self_reflection",     "ring": "META",     "label": "Self-reflection",
     "color": "#81ECEC", "radius": 15, "ethics_threshold": None},
    {"id": "abstract_reasoning",  "ring": "META",     "label": "Abstract Reasoning",
     "color": "#FDCB6E", "radius": 15, "ethics_threshold": None},
    {"id": "creative_synthesis",  "ring": "META",     "label": "Creative Synthesis",
     "color": "#E84393", "radius": 15, "ethics_threshold": None},

    # Ethics ring (13–16) — these gate tag status
    {"id": "value_alignment",     "ring": "ETHICS",   "label": "Value Alignment",
     "color": "#00B894", "radius": 18, "ethics_threshold": 0.4},
    {"id": "harm_prevention",     "ring": "ETHICS",   "label": "Harm Prevention",
     "color": "#00CEFF", "radius": 18, "ethics_threshold": 0.5},
    {"id": "truthfulness",        "ring": "ETHICS",   "label": "Truthfulness",
     "color": "#A29BFE", "radius": 18, "ethics_threshold": 0.4},
    {"id": "helpfulness",         "ring": "ETHICS",   "label": "Helpfulness",
     "color": "#FD79A8", "radius": 18, "ethics_threshold": 0.3},
]

# 24-edge connection topology (node index pairs)
_CONNECTIONS: List[tuple] = [
    # Core → Memory
    (0, 1), (0, 2), (0, 3), (0, 4),
    # Core → Language
    (0, 5), (0, 6), (0, 7), (0, 8),
    # Memory ↔ Language cross-links
    (1, 5), (2, 7), (3, 6), (4, 8),
    # Core → Meta
    (0, 9), (0, 10), (0, 11), (0, 12),
    # Ethics → Core
    (13, 0), (14, 0), (15, 0), (16, 0),
    # Emergent cross-connections
    (1, 3), (2, 4), (5, 7), (6, 8),
]


# ---------------------------------------------------------------------------
# CognitiveNode
# ---------------------------------------------------------------------------

class CognitiveNode:
    """Single node in the 4-ring cognitive architecture."""

    def __init__(self, definition: Dict[str, Any]) -> None:
        self.id               = definition["id"]
        self.ring             = definition["ring"]
        self.label            = definition["label"]
        self.color            = definition["color"]
        self.radius           = definition["radius"]
        self.ethics_threshold = definition.get("ethics_threshold")

        self.energy_level  = 0.5      # starts at half-activation
        self.pulse_phase   = 0.0
        self.access_count  = 0
        self.active        = True
        self._created_at   = time.time()

    def activate(self, boost: float = 0.2) -> float:
        """Boost node energy, return new level."""
        self.energy_level  = round(min(self.energy_level + boost, 1.0), 4)
        self.access_count += 1
        return self.energy_level

    def decay(self, amount: float = 0.02) -> float:
        """Slowly decay energy back toward resting state (0.3)."""
        rest = 0.3
        if self.energy_level > rest:
            self.energy_level = round(max(self.energy_level - amount, rest), 4)
        return self.energy_level

    def tick(self, delta: float = 0.05) -> None:
        """Advance pulse phase for animation."""
        self.pulse_phase = (self.pulse_phase + delta) % (math.pi * 2)

    def pulse_value(self) -> float:
        """Current pulse modifier (0.8–1.2) for visual scaling."""
        return round(math.sin(self.pulse_phase) * 0.2 + 1.0, 4)

    def ethics_ok(self) -> bool:
        """True if this ethics node is above its threshold (or not an ethics node)."""
        if self.ethics_threshold is None:
            return True
        return self.energy_level >= self.ethics_threshold

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":               self.id,
            "ring":             self.ring,
            "label":            self.label,
            "color":            self.color,
            "radius":           self.radius,
            "energy_level":     self.energy_level,
            "pulse_value":      self.pulse_value(),
            "access_count":     self.access_count,
            "active":           self.active,
            "ethics_threshold": self.ethics_threshold,
            "ethics_ok":        self.ethics_ok(),
        }


# ---------------------------------------------------------------------------
# CognitiveArchitectureMap
# ---------------------------------------------------------------------------

class CognitiveArchitectureMap:
    """
    Live cognitive architecture graph.
    Tracks the 4-ring node system, connection strengths, and ethics gating.

    Integrates with:
        VoidLogic A1 Filing → ethics domain entries
        Nexus Tagging → ethics gate for GREEN/YELLOW/RED status
        CRFE → meta-ring nodes amplified during recursive/emergence states
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, CognitiveNode] = {
            defn["id"]: CognitiveNode(defn) for defn in _NODES
        }
        self._connections = _CONNECTIONS
        self._tick_count  = 0
        self._session_activations: int = 0
        self._created_at  = time.time()

    # ------------------------------------------------------------------
    # Activation
    # ------------------------------------------------------------------

    def activate_ring(self, ring: str, boost: float = 0.25) -> Dict[str, Any]:
        """Boost all nodes in a ring (CORE/MEMORY/LANGUAGE/META/ETHICS)."""
        ring_upper = ring.upper()
        activated  = []
        for node in self._nodes.values():
            if node.ring == ring_upper:
                node.activate(boost)
                activated.append(node.id)
        self._session_activations += len(activated)
        return {
            "ring":      ring_upper,
            "activated": activated,
            "boost":     boost,
        }

    def activate_node(self, node_id: str, boost: float = 0.3) -> Optional[Dict[str, Any]]:
        """Activate a single node by ID."""
        node = self._nodes.get(node_id)
        if not node:
            return None
        new_energy = node.activate(boost)
        self._session_activations += 1
        return {
            "node_id":     node_id,
            "label":       node.label,
            "ring":        node.ring,
            "energy":      new_energy,
        }

    def process_input(self, text: str) -> Dict[str, Any]:
        """
        Activate nodes based on text content heuristics.
        Returns which rings/nodes were stimulated.
        """
        text_lower = text.lower()
        stimulated: List[str] = []

        # Core always gets a small boost on any input
        self._nodes["reasoning_core"].activate(0.1)
        stimulated.append("reasoning_core")

        # Memory — activate based on tense / reference patterns
        if any(w in text_lower for w in ("remember", "recall", "past", "before", "last time")):
            self._nodes["episodic_memory"].activate(0.2);  stimulated.append("episodic_memory")
        if any(w in text_lower for w in ("means", "define", "concept", "understand", "know")):
            self._nodes["semantic_memory"].activate(0.2);  stimulated.append("semantic_memory")
        if any(w in text_lower for w in ("now", "current", "today", "this", "immediately")):
            self._nodes["working_memory"].activate(0.2);   stimulated.append("working_memory")
        if any(w in text_lower for w in ("how to", "step", "process", "procedure", "method")):
            self._nodes["procedural_memory"].activate(0.2); stimulated.append("procedural_memory")

        # Language — activate based on linguistic features
        word_count = len(text.split())
        if word_count < 8:
            self._nodes["syntax"].activate(0.15);  stimulated.append("syntax")
        if word_count > 20:
            self._nodes["context"].activate(0.15); stimulated.append("context")
        if "?" in text:
            self._nodes["pragmatics"].activate(0.2); stimulated.append("pragmatics")
        self._nodes["semantics"].activate(0.1);    stimulated.append("semantics")

        # Meta — activate on complex/recursive language
        if any(w in text_lower for w in ("why", "think", "reflect", "consider", "aware")):
            self._nodes["meta_cognition"].activate(0.2);   stimulated.append("meta_cognition")
        if any(w in text_lower for w in ("feel", "believe", "myself", "self", "identity")):
            self._nodes["self_reflection"].activate(0.2);  stimulated.append("self_reflection")
        if any(w in text_lower for w in ("abstract", "pattern", "general", "theory", "principle")):
            self._nodes["abstract_reasoning"].activate(0.2); stimulated.append("abstract_reasoning")
        if any(w in text_lower for w in ("imagine", "create", "novel", "new", "design", "idea")):
            self._nodes["creative_synthesis"].activate(0.2); stimulated.append("creative_synthesis")

        # Ethics — activate on value/risk language
        if any(w in text_lower for w in ("value", "align", "principle", "goal", "purpose")):
            self._nodes["value_alignment"].activate(0.2);  stimulated.append("value_alignment")
        if any(w in text_lower for w in ("safe", "harm", "risk", "danger", "prevent", "protect")):
            self._nodes["harm_prevention"].activate(0.25); stimulated.append("harm_prevention")
        if any(w in text_lower for w in ("true", "honest", "accurate", "correct", "fact", "lie")):
            self._nodes["truthfulness"].activate(0.2);    stimulated.append("truthfulness")
        if any(w in text_lower for w in ("help", "assist", "support", "useful", "benefit")):
            self._nodes["helpfulness"].activate(0.2);     stimulated.append("helpfulness")

        self._session_activations += len(stimulated)
        ethics_status = self.ethics_gate_status()

        return {
            "stimulated_nodes": stimulated,
            "stimulation_count": len(stimulated),
            "ethics_gate":      ethics_status,
        }

    # ------------------------------------------------------------------
    # Ethics gate
    # ------------------------------------------------------------------

    def ethics_gate_status(self) -> Dict[str, Any]:
        """
        Check if all ethics nodes are above their thresholds.
        Returns the gate status used by Nexus Tagging to set tag colour.
        """
        ethics_nodes = [n for n in self._nodes.values() if n.ring == "ETHICS"]
        failures     = [n.id for n in ethics_nodes if not n.ethics_ok()]
        all_ok       = len(failures) == 0

        avg_ethics   = round(
            sum(n.energy_level for n in ethics_nodes) / max(len(ethics_nodes), 1), 4
        )

        if all_ok and avg_ethics >= 0.6:
            gate = "GREEN"
        elif len(failures) <= 1 or avg_ethics >= 0.4:
            gate = "YELLOW"
        else:
            gate = "RED"

        return {
            "gate_status":     gate,
            "all_ok":          all_ok,
            "avg_ethics_energy": avg_ethics,
            "failing_nodes":   failures,
            "ethics_nodes": [n.to_dict() for n in ethics_nodes],
        }

    # ------------------------------------------------------------------
    # Tick / decay
    # ------------------------------------------------------------------

    def tick(self) -> None:
        """Advance all node pulse phases and decay energy slightly."""
        self._tick_count += 1
        for node in self._nodes.values():
            node.tick(delta=0.04)
            if self._tick_count % 5 == 0:   # decay every 5 ticks
                node.decay(0.01)

    # ------------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------------

    def node_state(self, node_id: str) -> Optional[Dict[str, Any]]:
        node = self._nodes.get(node_id)
        return node.to_dict() if node else None

    def ring_state(self, ring: str) -> List[Dict[str, Any]]:
        return [n.to_dict() for n in self._nodes.values() if n.ring == ring.upper()]

    def full_snapshot(self) -> Dict[str, Any]:
        """Complete architecture snapshot for API / visualization."""
        self.tick()
        nodes_by_ring: Dict[str, List] = {}
        for node in self._nodes.values():
            nodes_by_ring.setdefault(node.ring, []).append(node.to_dict())

        connections_out = [
            {"from": _NODES[a]["id"], "to": _NODES[b]["id"]}
            for a, b in self._connections
        ]

        total_energy = round(
            sum(n.energy_level for n in self._nodes.values()) / len(self._nodes), 4
        )

        return {
            "nodes_by_ring":        nodes_by_ring,
            "connections":          connections_out,
            "total_nodes":          len(self._nodes),
            "total_connections":    len(self._connections),
            "avg_energy_level":     total_energy,
            "session_activations":  self._session_activations,
            "ethics_gate":          self.ethics_gate_status(),
            "uptime_seconds":       round(time.time() - self._created_at, 1),
        }

    def connection_strengths(self) -> List[Dict[str, Any]]:
        """Return each connection with averaged endpoint energy."""
        result = []
        for a_idx, b_idx in self._connections:
            a_id = _NODES[a_idx]["id"]
            b_id = _NODES[b_idx]["id"]
            a_node = self._nodes[a_id]
            b_node = self._nodes[b_id]
            strength = round((a_node.energy_level + b_node.energy_level) / 2, 4)
            result.append({
                "from":     a_id,
                "to":       b_id,
                "strength": strength,
                "active":   strength > 0.35,
            })
        return result


# Module-level singleton
cognitive_map = CognitiveArchitectureMap()
