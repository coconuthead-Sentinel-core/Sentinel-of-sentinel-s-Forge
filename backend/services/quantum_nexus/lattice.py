"""
Quantum Nexus Lattice
Python model of the sacred-geometry node network from the QuantumNexusSimulation
visualization. Tracks real activation state, connections, lattice expansion,
quantum flux, and engagement for the backend API.

Node topology — Metatron's Cube layout (11 nodes):
    center    — CORE NEXUS       (nexus type)
    challenge — CHALLENGE        (guide type)
    mirror    — MIRROR           (guide type)
    guide     — GUIDE            (guide type)
    emerge    — EMERGE           (emerge type)
    pool1     — POOL α           (pool type)
    pool2     — POOL β           (pool type)
    coconut   — COCONUT HEAD     (coconut type)
    shannon   — SHANNON          (protocol type)
    quantum   — QUANTUM FLUX     (quantum type)
    harmony   — HARMONY          (harmony type)

Connections follow the sacred geometry graph (18 edges).
"""
from __future__ import annotations

import math
import time
from typing import Dict, Any, List, Optional, Set


# ---------------------------------------------------------------------------
# Static topology
# ---------------------------------------------------------------------------

_NODES: List[Dict[str, Any]] = [
    {"id": "center",    "x": 50, "y": 50, "type": "nexus",    "label": "CORE NEXUS"},
    {"id": "challenge", "x": 25, "y": 25, "type": "guide",    "label": "CHALLENGE"},
    {"id": "mirror",    "x": 75, "y": 25, "type": "guide",    "label": "MIRROR"},
    {"id": "guide",     "x": 50, "y": 80, "type": "guide",    "label": "GUIDE"},
    {"id": "emerge",    "x": 75, "y": 75, "type": "emerge",   "label": "EMERGE"},
    {"id": "pool1",     "x": 15, "y": 50, "type": "pool",     "label": "POOL α"},
    {"id": "pool2",     "x": 85, "y": 50, "type": "pool",     "label": "POOL β"},
    {"id": "coconut",   "x": 25, "y": 75, "type": "coconut",  "label": "COCONUT HEAD"},
    {"id": "shannon",   "x": 50, "y": 15, "type": "protocol", "label": "SHANNON"},
    {"id": "quantum",   "x": 40, "y": 40, "type": "quantum",  "label": "QUANTUM FLUX"},
    {"id": "harmony",   "x": 60, "y": 60, "type": "harmony",  "label": "HARMONY"},
]

_CONNECTIONS: List[tuple] = [
    ("center",    "challenge"),
    ("center",    "mirror"),
    ("center",    "guide"),
    ("center",    "emerge"),
    ("center",    "pool1"),
    ("center",    "pool2"),
    ("challenge", "mirror"),
    ("mirror",    "guide"),
    ("guide",     "emerge"),
    ("emerge",    "challenge"),
    ("pool1",     "coconut"),
    ("pool2",     "shannon"),
    ("shannon",   "challenge"),
    ("coconut",   "guide"),
    ("quantum",   "center"),
    ("harmony",   "center"),
    ("quantum",   "harmony"),
    ("shannon",   "quantum"),
]

# Ordered activation sequence with status messages
_ACTIVATION_SEQUENCE: List[tuple] = [
    ("shannon",   "SHANNON PROTOCOLS ONLINE — INFORMATION THEORY ENGAGED"),
    ("coconut",   "COCONUT HEAD PROTOCOLS ACTIVATED — DIVINE HUMOR INFUSED"),
    ("pool1",     "POOL NEXUS α ESTABLISHED — CREATIVE FLOWS OPEN"),
    ("pool2",     "POOL NEXUS β ESTABLISHED — LOGIC MATRIX SYNCHRONIZED"),
    ("center",    "CORE NEXUS SYNCHRONIZING — QUANTUM FIELD STABILIZING"),
    ("challenge", "CHALLENGE MATRIX INITIALIZED — GROWTH POTENTIAL MAXIMIZED"),
    ("mirror",    "MIRROR PROTOCOLS ACTIVE — SELF-REFLECTION AMPLIFIED"),
    ("guide",     "GUIDANCE SYSTEMS OPERATIONAL — WISDOM CHANNELS OPEN"),
    ("emerge",    "EMERGENCE FIELD STABILIZED — TRANSFORMATION IMMINENT"),
    ("quantum",   "QUANTUM FLUX MODULATOR ONLINE — ENTANGLEMENT ESTABLISHED"),
    ("harmony",   "HARMONIC CONVERGENCE ACHIEVED — RESONANCE AT PEAK"),
]

# Colour palette per node type (for API consumers / frontend rendering)
_NODE_COLORS: Dict[str, str] = {
    "nexus":    "rgba(255, 215, 0, {a})",    # Gold
    "guide":    "rgba(0, 255, 255, {a})",    # Cyan
    "emerge":   "rgba(255, 105, 180, {a})",  # Pink
    "pool":     "rgba(50, 205, 50, {a})",    # Lime
    "coconut":  "rgba(255, 165, 0, {a})",    # Orange
    "protocol": "rgba(138, 43, 226, {a})",   # Purple
    "quantum":  "rgba(70, 130, 180, {a})",   # Steel blue
    "harmony":  "rgba(255, 99, 71, {a})",    # Tomato
}


# ---------------------------------------------------------------------------
# Lattice class
# ---------------------------------------------------------------------------

class QuantumNexusLattice:
    """
    Backend model of the Quantum Nexus sacred geometry lattice.
    Tracks node activation state, lattice expansion, quantum flux,
    and user engagement as real server-side state.
    """

    def __init__(self) -> None:
        self._active_nodes: Set[str] = set()
        self._protocols_active: bool = False
        self._lattice_expanded: bool = False
        self._quantum_flux: float    = 0.0
        self._user_engagement: float = 0.0
        self._status: str            = "STANDBY — LATTICE DORMANT"
        self._activation_log: List[Dict[str, Any]] = []
        self._created_at: float      = time.time()
        self._flux_tick: float       = 0.0   # simulated tick for flux calculation

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def activate_protocols(self) -> Dict[str, Any]:
        """
        Activate all nodes in the canonical sequence.
        Returns the full activation log and final status.
        """
        if self._protocols_active:
            return {
                "already_active": True,
                "status":         self._status,
                "active_nodes":   list(self._active_nodes),
            }

        self._activation_log.clear()
        self._user_engagement = min(self._user_engagement + 25, 100)

        for node_id, status_msg in _ACTIVATION_SEQUENCE:
            self._active_nodes.add(node_id)
            self._status = status_msg
            self._user_engagement = min(self._user_engagement + 5, 100)
            self._activation_log.append({
                "node_id": node_id,
                "status":  status_msg,
                "t":       round(time.time(), 3),
            })

        self._protocols_active = True
        self._status = "ALL SYSTEMS ONLINE — LATTICE EXPANSION READY"

        return {
            "already_active":   False,
            "protocols_active": True,
            "active_nodes":     list(self._active_nodes),
            "user_engagement":  self._user_engagement,
            "status":           self._status,
            "activation_log":   self._activation_log,
        }

    def activate_node(self, node_id: str) -> Dict[str, Any]:
        """Activate a single node by ID."""
        ids = {n["id"] for n in _NODES}
        if node_id not in ids:
            return {"error": f"Unknown node '{node_id}'", "valid_ids": sorted(ids)}
        self._active_nodes.add(node_id)
        self._user_engagement = min(self._user_engagement + 5, 100)
        return {
            "activated": node_id,
            "active_nodes": list(self._active_nodes),
            "user_engagement": self._user_engagement,
        }

    def toggle_lattice(self) -> Dict[str, Any]:
        """Expand or contract the lattice (requires protocols active)."""
        if not self._protocols_active:
            return {"error": "Protocols not yet active. Activate protocols first."}
        self._lattice_expanded = not self._lattice_expanded
        self._user_engagement = min(self._user_engagement + 10, 100)
        self._status = (
            "LATTICE FULLY EXPANDED — QUANTUM FIELD AT MAXIMUM CAPACITY"
            if self._lattice_expanded
            else "LATTICE CONTRACTED — ENERGY CONSERVATION MODE"
        )
        return {
            "lattice_expanded": self._lattice_expanded,
            "status":           self._status,
            "user_engagement":  self._user_engagement,
        }

    def reset(self) -> Dict[str, Any]:
        """Reset the lattice to dormant state."""
        self._active_nodes.clear()
        self._protocols_active = False
        self._lattice_expanded = False
        self._quantum_flux     = 0.0
        self._user_engagement  = 0.0
        self._flux_tick        = 0.0
        self._status           = "STANDBY — LATTICE DORMANT"
        self._activation_log.clear()
        return {"reset": True, "status": self._status}

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def tick(self, delta: float = 0.2) -> None:
        """Advance the internal simulation clock (call this on each status poll)."""
        self._flux_tick = (self._flux_tick + delta) % 100
        if self._protocols_active:
            self._quantum_flux = self._flux_tick

    def status(self) -> Dict[str, Any]:
        """Full lattice state snapshot."""
        self.tick()
        active_list = list(self._active_nodes)
        node_states = []
        for node in _NODES:
            is_active = node["id"] in self._active_nodes
            color_tpl = _NODE_COLORS.get(node["type"], "rgba(255,255,255,{a})")
            alpha     = "0.9" if is_active else "0.25"
            node_states.append({
                **node,
                "active":       is_active,
                "color":        color_tpl.format(a=alpha),
            })

        active_connections = [
            {"from": f, "to": t}
            for f, t in _CONNECTIONS
            if f in self._active_nodes and t in self._active_nodes
        ]

        return {
            "status":            self._status,
            "protocols_active":  self._protocols_active,
            "lattice_expanded":  self._lattice_expanded,
            "quantum_flux":      round(self._quantum_flux, 2),
            "user_engagement":   round(self._user_engagement, 2),
            "active_node_count": len(active_list),
            "total_nodes":       len(_NODES),
            "active_nodes":      active_list,
            "nodes":             node_states,
            "connections":       [{"from": f, "to": t} for f, t in _CONNECTIONS],
            "active_connections":active_connections,
            "uptime_seconds":    round(time.time() - self._created_at, 1),
        }

    def topology(self) -> Dict[str, Any]:
        """Return the static topology (nodes + connections + colour palette)."""
        return {
            "nodes":       _NODES,
            "connections": [{"from": f, "to": t} for f, t in _CONNECTIONS],
            "colors":      _NODE_COLORS,
            "activation_sequence": [
                {"node_id": nid, "status": msg}
                for nid, msg in _ACTIVATION_SEQUENCE
            ],
        }

    def node_info(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Return static info for a single node."""
        for node in _NODES:
            if node["id"] == node_id:
                neighbours = [
                    t for f, t in _CONNECTIONS if f == node_id
                ] + [
                    f for f, t in _CONNECTIONS if t == node_id
                ]
                return {**node, "neighbours": list(set(neighbours))}
        return None


# Module-level singleton
lattice = QuantumNexusLattice()
