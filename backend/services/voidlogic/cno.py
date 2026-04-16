"""
ComputeNodeRouter (CNO)
Live orchestration layer that wraps the Dynamic Node Constructor (DNC)
and provides real-time payload routing, load balancing, and node stack health
monitoring. Decides where each incoming payload gets routed and ensures no node
stack overloads or deadlocks.

Responsibilities:
    • Accept a payload and assign it to the optimal node stack
    • Monitor load across all active stacks and trigger auto-scaling
    • Discharge idle stacks on a configurable interval
    • Emit a health pulse for the topology renderer
"""
from __future__ import annotations

import time
from typing import Dict, Any, List, Optional

from .node_geometry import dnc, TETRAHEDRAL, OCTAHEDRAL, ICOSAHEDRAL


# How often (seconds) the overlay runs a passive discharge cycle
_DISCHARGE_INTERVAL = 60.0
# Threshold above which a stack is considered overloaded
_OVERLOAD_THRESHOLD = 0.80


class ComputeNodeRouter:
    """Compute Node Router — live routing and load management."""

    def __init__(self) -> None:
        self._last_discharge: float = time.time()
        self._routed_total: int = 0
        self._overload_events: int = 0
        self._routing_log: List[Dict[str, Any]] = []   # last 50 events

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route_payload(
        self,
        payload: str,
        complexity: float = 0.5,
        stack_id: str = "primary",
    ) -> Dict[str, Any]:
        """
        Route a symbolic payload through the appropriate node tier.
        Auto-discharges idle nodes before routing.
        """
        self._maybe_discharge()

        result = dnc.route(complexity, stack_id)
        self._routed_total += 1

        overloaded = False
        if result["routed"] and result.get("symbolic_load_after", 0) >= _OVERLOAD_THRESHOLD:
            overloaded = True
            self._overload_events += 1
            # Auto-spawn a relief stack
            relief_id = f"relief_{int(time.time()) % 10000}"
            dnc.spawn_stack(relief_id, layers=3)

        entry = {
            "timestamp":  round(time.time(), 3),
            "stack_id":   stack_id,
            "complexity": complexity,
            "result":     result,
            "overloaded": overloaded,
        }
        self._routing_log = (self._routing_log + [entry])[-50:]

        return {
            "routed":          result.get("routed", False),
            "node_id":         result.get("node_id"),
            "tier":            result.get("tier"),
            "load_after":      result.get("symbolic_load_after"),
            "overflow":        result.get("overflow", 0),
            "overload_event":  overloaded,
            "total_routed":    self._routed_total,
        }

    def health_pulse(self) -> Dict[str, Any]:
        """
        Return a real-time health snapshot of the entire node fabric.
        Used by STVL for visualization and by the engine for decision-making.
        """
        snapshot = dnc.full_snapshot()
        stacks = snapshot["stacks"]

        stack_health = {}
        for sid, data in stacks.items():
            avg = data.get("avg_load", 0.0)
            stack_health[sid] = {
                "avg_load":     avg,
                "status":       "OVERLOADED" if avg >= _OVERLOAD_THRESHOLD
                                else "ACTIVE" if avg > 0
                                else "IDLE",
                "total_nodes":  data.get("total_nodes", 0),
            }

        overall = (
            "CRITICAL"  if any(s["status"] == "OVERLOADED" for s in stack_health.values()) else
            "ACTIVE"    if any(s["status"] == "ACTIVE"     for s in stack_health.values()) else
            "IDLE"
        )

        return {
            "overall_status":  overall,
            "total_stacks":    snapshot["total_stacks"],
            "stack_health":    stack_health,
            "routed_total":    self._routed_total,
            "overload_events": self._overload_events,
            "last_discharge":  round(self._last_discharge, 3),
        }

    def get_routing_log(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self._routing_log[-limit:]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _maybe_discharge(self) -> None:
        now = time.time()
        if now - self._last_discharge >= _DISCHARGE_INTERVAL:
            dnc.discharge_all(amount=0.1)
            self._last_discharge = now


# Module-level singleton
cno = ComputeNodeRouter()
