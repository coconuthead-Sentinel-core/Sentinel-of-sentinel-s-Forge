"""
VoidLogic Node Geometry System
Three-tier geometrically optimized node architecture:

    TETRAHEDRAL  — 3 connection points, minimal overhead, rapid symbolic transfer
                   Used for: primary processing, low-complexity tasks, speed-critical paths

    OCTAHEDRAL   — 6 connection points, multi-directional recursion
                   Used for: recursive logic, parallel threading, symbolic mapping

    ICOSAHEDRAL  — 20 connection points, maximum symbolic complexity
                   Used for: deep synthesis, cross-domain threading, emergent pattern detection

Nodes stack vertically in fractal tetrahedral layers.
Horizontal scaling uses octahedral grids.
Dynamic Node Constructor (DNC) reconfigures geometry in real time.
"""
from __future__ import annotations

import math
import time
import uuid
from typing import Dict, Any, List, Optional


# Node tier constants
TETRAHEDRAL  = "TETRAHEDRAL"   # 3 connections — speed tier
OCTAHEDRAL   = "OCTAHEDRAL"    # 6 connections — recursion tier
ICOSAHEDRAL  = "ICOSAHEDRAL"   # 20 connections — synthesis tier

_CONNECTIONS = {
    TETRAHEDRAL:  3,
    OCTAHEDRAL:   6,
    ICOSAHEDRAL:  20,
}

_COMPLEXITY_THRESHOLD = {
    TETRAHEDRAL:  (0.0, 0.40),
    OCTAHEDRAL:   (0.40, 0.70),
    ICOSAHEDRAL:  (0.70, 1.0),
}


class GeometricNode:
    """A single node in the VoidLogic node stack."""

    def __init__(self, geometry: str, layer: int, stack_id: str) -> None:
        self.id           = str(uuid.uuid4())[:8]
        self.geometry     = geometry
        self.layer        = layer
        self.stack_id     = stack_id
        self.max_connections = _CONNECTIONS[geometry]
        self.connections: List[str] = []          # connected node IDs
        self.symbolic_load: float = 0.0           # 0.0 - 1.0
        self.active       = True
        self.created_at   = time.time()
        self.process_count = 0

    def connect(self, node_id: str) -> bool:
        if len(self.connections) < self.max_connections and node_id not in self.connections:
            self.connections.append(node_id)
            return True
        return False

    def process(self, load: float) -> float:
        """Accept symbolic load, return overflow."""
        capacity = 1.0 - self.symbolic_load
        accepted = min(load, capacity)
        self.symbolic_load = round(self.symbolic_load + accepted, 4)
        self.process_count += 1
        return round(load - accepted, 4)

    def discharge(self, amount: float = 0.1) -> None:
        self.symbolic_load = round(max(0.0, self.symbolic_load - amount), 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":             self.id,
            "geometry":       self.geometry,
            "layer":          self.layer,
            "stack_id":       self.stack_id,
            "max_connections": self.max_connections,
            "connections":    self.connections,
            "symbolic_load":  self.symbolic_load,
            "active":         self.active,
            "process_count":  self.process_count,
        }


class NodeStack:
    """
    A vertical fractal stack of geometric nodes.
    Layers ascend in complexity: Tetrahedral → Octahedral → Icosahedral.
    """

    def __init__(self, stack_id: str, layers: int = 3) -> None:
        self.stack_id = stack_id
        self.nodes: List[GeometricNode] = []
        self._build(layers)

    def _build(self, layers: int) -> None:
        for layer in range(layers):
            # Assign geometry by layer depth
            if layer == 0:
                geometry = TETRAHEDRAL
                count = 4
            elif layer == 1:
                geometry = OCTAHEDRAL
                count = 2
            else:
                geometry = ICOSAHEDRAL
                count = 1

            layer_nodes = [GeometricNode(geometry, layer, self.stack_id) for _ in range(count)]
            self.nodes.extend(layer_nodes)

            # Connect within layer
            for i, node in enumerate(layer_nodes[:-1]):
                node.connect(layer_nodes[i+1].id)

    def route(self, complexity: float) -> Dict[str, Any]:
        """
        Route a symbolic payload of given complexity through the stack.
        Returns routing report.
        """
        # Select node tier by complexity
        tier = self._select_tier(complexity)
        tier_nodes = [n for n in self.nodes if n.geometry == tier and n.active]

        if not tier_nodes:
            return {"routed": False, "reason": "No active nodes in selected tier", "tier": tier}

        # Route to least-loaded node
        target = min(tier_nodes, key=lambda n: n.symbolic_load)
        overflow = target.process(complexity)

        return {
            "routed": True,
            "node_id": target.id,
            "tier": tier,
            "symbolic_load_after": target.symbolic_load,
            "overflow": overflow,
            "layer": target.layer,
        }

    def _select_tier(self, complexity: float) -> str:
        for tier, (low, high) in _COMPLEXITY_THRESHOLD.items():
            if low <= complexity < high:
                return tier
        return ICOSAHEDRAL

    def snapshot(self) -> Dict[str, Any]:
        return {
            "stack_id": self.stack_id,
            "total_nodes": len(self.nodes),
            "by_geometry": {
                TETRAHEDRAL:  [n.to_dict() for n in self.nodes if n.geometry == TETRAHEDRAL],
                OCTAHEDRAL:   [n.to_dict() for n in self.nodes if n.geometry == OCTAHEDRAL],
                ICOSAHEDRAL:  [n.to_dict() for n in self.nodes if n.geometry == ICOSAHEDRAL],
            },
            "avg_load": round(
                sum(n.symbolic_load for n in self.nodes) / max(len(self.nodes), 1), 4
            ),
        }


class DynamicNodeConstructor:
    """
    Real-time node stack manager.
    Spawns, expands, contracts, and reconfigures stacks on demand.
    """

    def __init__(self) -> None:
        self._stacks: Dict[str, NodeStack] = {}
        self._spawn_default()

    def _spawn_default(self) -> None:
        """Create the initial primary stack."""
        self._stacks["primary"] = NodeStack("primary", layers=3)

    def spawn_stack(self, stack_id: str = None, layers: int = 3) -> Dict[str, Any]:
        sid = stack_id or f"stack_{len(self._stacks)+1}"
        self._stacks[sid] = NodeStack(sid, layers=layers)
        return {"spawned": sid, "layers": layers, "total_stacks": len(self._stacks)}

    def route(self, complexity: float, stack_id: str = "primary") -> Dict[str, Any]:
        if stack_id not in self._stacks:
            # Auto-spawn if needed
            self.spawn_stack(stack_id)
        return self._stacks[stack_id].route(complexity)

    def discharge_all(self, amount: float = 0.1) -> None:
        for stack in self._stacks.values():
            for node in stack.nodes:
                node.discharge(amount)

    def full_snapshot(self) -> Dict[str, Any]:
        return {
            "total_stacks": len(self._stacks),
            "stacks": {sid: s.snapshot() for sid, s in self._stacks.items()},
        }


# Module-level singleton
dnc = DynamicNodeConstructor()
