"""
Quantum Nexus Lattice
Python model of the geometric node network from the QuantumNexusSimulation
visualization. Tracks real activation state, connections, lattice expansion,
flux, and engagement for the backend API.

Node topology — 11-node hexagonal lattice:
    center       — CORE NEXUS       (nexus type)
    challenge    — CHALLENGE        (guide type)
    mirror       — MIRROR           (guide type)
    guide        — GUIDE            (guide type)
    emerge       — EMERGE           (emerge type)
    pool1        — POOL A           (pool type)
    pool2        — POOL B           (pool type)
    bridge       — BRIDGE NODE      (bridge type)
    orchestrator — ORCHESTRATOR     (protocol type)
    quantum      — QUANTUM FLUX     (quantum type)
    harmony      — HARMONY          (harmony type)

Connections follow the standard lattice graph (18 edges).
"""
from __future__ import annotations

import math
import time
from typing import Dict, Any, List, Optional, Set


# ---------------------------------------------------------------------------
# Static topology
# ---------------------------------------------------------------------------

_NODES: List[Dict[str, Any]] = [
    {"id": "center",       "x": 50, "y": 50, "type": "nexus",    "label": "CORE NEXUS"},
    {"id": "challenge",    "x": 25, "y": 25, "type": "guide",    "label": "CHALLENGE"},
    {"id": "mirror",       "x": 75, "y": 25, "type": "guide",    "label": "MIRROR"},
    {"id": "guide",        "x": 50, "y": 80, "type": "guide",    "label": "GUIDE"},
    {"id": "emerge",       "x": 75, "y": 75, "type": "emerge",   "label": "EMERGE"},
    {"id": "pool1",        "x": 15, "y": 50, "type": "pool",     "label": "POOL A"},
    {"id": "pool2",        "x": 85, "y": 50, "type": "pool",     "label": "POOL B"},
    {"id": "bridge",       "x": 25, "y": 75, "type": "bridge",   "label": "BRIDGE NODE"},
    {"id": "orchestrator", "x": 50, "y": 15, "type": "protocol", "label": "ORCHESTRATOR"},
    {"id": "quantum",      "x": 40, "y": 40, "type": "quantum",  "label": "QUANTUM FLUX"},
    {"id": "harmony",      "x": 60, "y": 60, "type": "harmony",  "label": "HARMONY"},
]

_CONNECTIONS: List[tuple] = [
    ("center",       "challenge"),
    ("center",       "mirror"),
    ("center",       "guide"),
    ("center",       "emerge"),
    ("center",       "pool1"),
    ("center",       "pool2"),
    ("challenge",    "mirror"),
    ("mirror",       "guide"),
    ("guide",        "emerge"),
    ("emerge",       "challenge"),
    ("pool1",        "bridge"),
    ("pool2",        "orchestrator"),
    ("orchestrator", "challenge"),
    ("bridge",       "guide"),
    ("quantum",      "center"),
    ("harmony",      "center"),
    ("quantum",      "harmony"),
    ("orchestrator", "quantum"),
]

# Ordered activation sequence with status messages
_ACTIVATION_SEQUENCE: List[tuple] = [
    ("orchestrator", "ORCHESTRATOR ONLINE — ROUTING PROTOCOLS ENGAGED"),
    ("bridge",       "BRIDGE NODE ACTIVE — CROSS-DOMAIN LINKS ESTABLISHED"),
    ("pool1",        "POOL A ESTABLISHED — PROCESSING STREAMS OPEN"),
    ("pool2",        "POOL B ESTABLISHED — LOGIC MATRIX SYNCHRONIZED"),
    ("center",       "CORE NEXUS SYNCHRONIZING — SYSTEM STABILIZING"),
    ("challenge",    "CHALLENGE MATRIX INITIALIZED — VALIDATION ACTIVE"),
    ("mirror",       "MIRROR NODE ACTIVE — CONTEXT RECALIBRATION ENABLED"),
    ("guide",        "GUIDANCE SYSTEMS OPERATIONAL — ROUTING CHANNELS OPEN"),
    ("emerge",       "EMERGENCE NODE STABLE — PATTERN DETECTION ACTIVE"),
    ("quantum",      "QUANTUM FLUX MODULATOR ONLINE — PROCESSING ESTABLISHED"),
    ("harmony",      "HARMONIC NODE SYNCHRONIZED — SYSTEM AT FULL CAPACITY"),
]

# Colour palette per node type (for API consumers / frontend rendering)
_NODE_COLORS: Dict[str, str] = {
    "nexus":    "rgba(255, 215, 0, {alpha})",    # Gold
    "guide":    "rgba(0, 255, 255, {alpha})",    # Cyan
    "emerge":   "rgba(255, 105, 180, {alpha})",  # Pink
    "pool":     "rgba(50, 205, 50, {alpha})",    # Lime
    "bridge":   "rgba(255, 165, 0, {alpha})",    # Orange
    "protocol": "rgba(138, 43, 226, {alpha})",   # Purple
    "quantum":  "rgba(70, 130, 180, {alpha})",   # Steel blue
    "harmony":  "rgba(255, 99, 71, {alpha})",    # Tomato
}


# ---------------------------------------------------------------------------
# Lattice class
# ---------------------------------------------------------------------------

class QuantumNexusLattice:
    """
    Backend model of the Quantum Nexus geometric node lattice.
    Tracks node activation state, lattice expansion, flux,
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
            "activated":       node_id,
            "active_nodes":    list(self._active_nodes),
            "user_engagement": self._user_engagement,
        }

    def toggle_lattice(self) -> Dict[str, Any]:
        """Expand or contract the lattice (requires protocols active)."""
        if not self._protocols_active:
            return {"error": "Protocols not yet active. Activate protocols first."}
        self._lattice_expanded = not self._lattice_expanded
        self._user_engagement = min(self._user_engagement + 10, 100)
        self._status = (
            "LATTICE FULLY EXPANDED — PROCESSING AT MAXIMUM CAPACITY"
            if self._lattice_expanded
            else "LATTICE CONTRACTED — CONSERVATION MODE"
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
            color_tpl = _NODE_COLORS.get(node["type"], "rgba(255,255,255,{alpha})")
            alpha     = "0.9" if is_active else "0.25"
            node_states.append({
                **node,
                "active": is_active,
                "color":  color_tpl.format(alpha=alpha),
            })

        active_connections = [
            {"from": f, "to": t}
            for f, t in _CONNECTIONS
            if f in self._active_nodes and t in self._active_nodes
        ]

        return {
            "status":             self._status,
            "protocols_active":   self._protocols_active,
            "lattice_expanded":   self._lattice_expanded,
            "quantum_flux":       round(self._quantum_flux, 2),
            "user_engagement":    round(self._user_engagement, 2),
            "active_node_count":  len(active_list),
            "total_nodes":        len(_NODES),
            "active_nodes":       active_list,
            "nodes":              node_states,
            "connections":        [{"from": f, "to": t} for f, t in _CONNECTIONS],
            "active_connections": active_connections,
            "uptime_seconds":     round(time.time() - self._created_at, 1),
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
