"""
STVL — Symbolic-Topology Visualization Layer
Renders the internal state of VoidLogic as a structured symbolic map
that can be consumed by a frontend visualizer, dashboard, or debug panel.

The STVL does not produce graphics — it produces a data payload that
describes the topology: nodes, edges, layers, load states, domain threads,
tesseract cells, and emergent signals. The frontend can render this
however it chooses (force graph, 3D hypercube, etc.).

Output sections:
    node_fabric     — all node stacks and their geometric tiers
    tesseract_map   — hyperplane snapshot of the 4D storage
    bridge_map      — active trans-domain wisdom threads
    crfe_pulse      — latest CRFE analysis result
    a1_index        — filing system snapshot
    cno_pulse       — CNO health pulse
    meta            — timestamp, engine version, render_mode
"""
from __future__ import annotations

import time
from typing import Dict, Any, Optional

from .node_geometry  import dnc
from .tesseract_storage import tesseract
from .bridge_wisdom  import bwt
from .a1_filing      import a1
from .cno            import cno
from .crfe           import crfe


_ENGINE_VERSION = "VoidLogic-5.0-IWE"


class STVL:
    """Symbolic-Topology Visualization Layer."""

    def render(
        self,
        crfe_input: Optional[str] = None,
        render_mode: str = "full",
    ) -> Dict[str, Any]:
        """
        Render the full VoidLogic topology.

        Args:
            crfe_input:  If provided, run a fresh CRFE analysis on this text.
            render_mode: 'full' | 'lite' — lite omits per-node details.

        Returns:
            A structured topology payload.
        """
        node_fabric   = self._render_node_fabric(render_mode)
        tesseract_map = self._render_tesseract()
        bridge_map    = self._render_bridges(render_mode)
        a1_index      = self._render_a1()
        cno_pulse     = cno.health_pulse()
        crfe_pulse    = crfe.process(crfe_input) if crfe_input else {"note": "no input provided"}

        return {
            "meta": {
                "timestamp":    round(time.time(), 3),
                "engine":       _ENGINE_VERSION,
                "render_mode":  render_mode,
            },
            "node_fabric":    node_fabric,
            "tesseract_map":  tesseract_map,
            "bridge_map":     bridge_map,
            "a1_index":       a1_index,
            "cno_pulse":      cno_pulse,
            "crfe_pulse":     crfe_pulse,
        }

    def lite_render(self) -> Dict[str, Any]:
        """Quick health snapshot — minimal data for dashboards."""
        cno_pulse = cno.health_pulse()
        snapshot  = dnc.full_snapshot()

        avg_loads = [
            s.get("avg_load", 0.0)
            for s in snapshot["stacks"].values()
        ]
        global_avg = round(sum(avg_loads) / max(len(avg_loads), 1), 4)

        return {
            "meta": {
                "timestamp": round(time.time(), 3),
                "engine":    _ENGINE_VERSION,
                "mode":      "lite",
            },
            "overall_status":    cno_pulse["overall_status"],
            "total_stacks":      cno_pulse["total_stacks"],
            "global_avg_load":   global_avg,
            "routed_total":      cno_pulse["routed_total"],
            "overload_events":   cno_pulse["overload_events"],
            "active_threads":    bwt.weave_snapshot()["active_threads"],
            "total_filings":     a1.index_snapshot()["total_filings"],
            "tesseract_stored":  tesseract.hyperplane_snapshot()["total_stored"],
        }

    # ------------------------------------------------------------------
    # Private renderers
    # ------------------------------------------------------------------

    def _render_node_fabric(self, mode: str) -> Dict[str, Any]:
        snapshot = dnc.full_snapshot()
        if mode == "lite":
            return {
                "total_stacks": snapshot["total_stacks"],
                "stacks": {
                    sid: {"avg_load": s["avg_load"], "total_nodes": s["total_nodes"]}
                    for sid, s in snapshot["stacks"].items()
                },
            }
        return snapshot

    def _render_tesseract(self) -> Dict[str, Any]:
        return tesseract.hyperplane_snapshot()

    def _render_bridges(self, mode: str) -> Dict[str, Any]:
        ws = bwt.weave_snapshot()
        if mode == "lite":
            return {
                "active_threads":     ws["active_threads"],
                "total_translations": ws["total_translations"],
            }
        return {**ws, "threads": bwt.active_threads()}

    def _render_a1(self) -> Dict[str, Any]:
        return a1.index_snapshot()


# Module-level singleton
stvl = STVL()
