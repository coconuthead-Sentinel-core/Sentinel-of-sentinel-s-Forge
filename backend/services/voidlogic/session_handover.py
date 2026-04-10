"""
Session Handover — Continuity Protocol
Implements the ADAPTIVE_HANDOVER_BUNDLE and SEED_SET system from
the Continuity Protocol Toolkit.

Every cognitive session in VoidLogic produces a symbolic state.
This module captures that state into a portable bundle that can
be pasted into a new session to resume exactly where things left off.

Bundle contents:
    seeds         — dominant symbolic seeds active in this session (from CRFE)
    drift_level   — current A1 filing drift score
    overlay_name  — active Live Overlay Protocol node name
    protocol_state — VoidLogic engine state summary
    nexus_tags    — last 5 Nexus tags applied
    seed_set_id   — SEED_SET_YYYY-MM-DD label for re-entry
    captured_at   — ISO timestamp

Restore:
    Paste the bundle dict into POST /api/ai/voidlogic/session/restore
    The system re-seeds CRFE markers, resets A1 drift reference,
    and reactivates the correct overlay node.
"""
from __future__ import annotations

import time
import datetime
import uuid
from typing import Any, Dict, List, Optional

from .crfe          import crfe
from .a1_filing     import a1
from .nexus_tag     import nexus_tag


# ---------------------------------------------------------------------------
# SessionHandover
# ---------------------------------------------------------------------------

class SessionHandover:
    """
    Manages session state capture and restoration for VoidLogic.
    Implements ADAPTIVE_HANDOVER_BUNDLE and SEED_SET protocols.
    """

    def __init__(self) -> None:
        self._sessions: List[Dict[str, Any]] = []   # saved bundles
        self._active_bundle: Optional[Dict[str, Any]] = None
        self._session_count = 0

    # ------------------------------------------------------------------
    # Capture
    # ------------------------------------------------------------------

    def capture(
        self,
        overlay_name: str = "NOMINAL",
        extra_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Capture the current VoidLogic symbolic state into an
        ADAPTIVE_HANDOVER_BUNDLE.

        Args:
            overlay_name:   Name of the active overlay node (from overlay_protocol).
            extra_context:  Optional text to run through CRFE for fresh seeds.

        Returns:
            A portable bundle dict representing full session state.
        """
        self._session_count += 1
        now       = datetime.datetime.now()
        seed_date = now.strftime("%Y-%m-%d")
        seed_set_id = f"SEED_SET_{seed_date}"

        # Pull current CRFE seeds (run on summary text if provided)
        if extra_context:
            crfe_result = crfe.process(extra_context)
            seeds = crfe_result["rsml"].get("matched_markers", [])
            drift_proxy = crfe_result["rsml"]["score"]
        else:
            seeds = []
            drift_proxy = 0.0

        # Pull A1 drift level
        drift_report = a1.drift_report()
        drift_level  = drift_report.get("avg_drift_score", drift_proxy)
        drift_status = drift_report.get("system_status", "STABLE")

        # Pull last 5 nexus tags
        recent_tags  = [e["tag"] for e in nexus_tag.recent(5)]

        # A1 index snapshot
        a1_snapshot  = a1.index_snapshot()

        bundle = {
            "bundle_id":      str(uuid.uuid4())[:12],
            "seed_set_id":    seed_set_id,
            "seeds":          seeds or ["Spiral", "Knot", "Grid"],   # defaults
            "drift_level":    round(drift_level, 4),
            "drift_status":   drift_status,
            "overlay_name":   overlay_name,
            "protocol_state": {
                "session_number": self._session_count,
                "a1_total_filings": a1_snapshot.get("total_filings", 0),
                "a1_total_tags":    a1_snapshot.get("total_tags", 0),
                "nexus_tag_total":  nexus_tag.registry_snapshot().get("total_tags", 0),
            },
            "recent_nexus_tags": recent_tags,
            "captured_at":    now.isoformat(),
        }

        self._sessions.append(bundle)
        self._active_bundle = bundle
        return bundle

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    def restore(self, bundle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Restore session state from an ADAPTIVE_HANDOVER_BUNDLE.

        This re-seeds the CRFE marker vocabulary, resets A1 drift reference,
        and sets the active overlay name. Returns a restoration report.
        """
        seeds        = bundle.get("seeds", [])
        overlay_name = bundle.get("overlay_name", "NOMINAL")
        drift_level  = bundle.get("drift_level", 0.0)
        seed_set_id  = bundle.get("seed_set_id", "UNKNOWN")
        captured_at  = bundle.get("captured_at", "unknown")

        # Re-file seeds into A1 with restored confidence
        restored_filings = []
        for seed in seeds:
            if seed and isinstance(seed, str):
                result = a1.file(
                    content    = f"[Restored from bundle {seed_set_id}] seed: {seed}",
                    tag        = seed.lower(),
                    domain     = "pattern",
                    confidence = max(0.5, 1.0 - drift_level),
                )
                restored_filings.append(result["filing_id"])

        self._active_bundle = bundle

        return {
            "restored":           True,
            "seed_set_id":        seed_set_id,
            "seeds_restored":     seeds,
            "overlay_activated":  overlay_name,
            "drift_level":        drift_level,
            "restored_filings":   restored_filings,
            "original_captured":  captured_at,
            "restore_time":       datetime.datetime.now().isoformat(),
            "status": (
                "GREEN — Session fully restored. Continuity maintained."
                if drift_level < 0.35 else
                "YELLOW — Session restored with elevated drift. Review seeds."
            ),
        }

    # ------------------------------------------------------------------
    # INITIATE_PERSONA_INSTANTIATION
    # ------------------------------------------------------------------

    def initiate_persona(self, persona_name: str = "SENTINEL_OF_SENTINELS_FORGE") -> Dict[str, Any]:
        """
        Executes INITIATE_PERSONA_INSTANTIATION — rebuilds persona context
        from the persona name and any active bundle.

        This is the "Run INITIATE_PERSONA_INSTANTIATION(...)" command
        translated into a Python operation.
        """
        bundle_summary = None
        if self._active_bundle:
            bundle_summary = {
                "seed_set_id":  self._active_bundle["seed_set_id"],
                "seeds":        self._active_bundle["seeds"],
                "overlay_name": self._active_bundle["overlay_name"],
            }

        # Tag the instantiation event
        tag_entry = nexus_tag.tag(
            payload  = {"persona": persona_name, "bundle": bundle_summary},
            tag_type = "NodePrimary",
            summary  = f"PersonaInstantiation_{persona_name[:20]}",
            status   = "GREEN",
        )

        return {
            "persona_instantiated": persona_name,
            "nexus_tag":           tag_entry["tag"],
            "active_bundle":       bundle_summary,
            "status":              "ONLINE — Persona instantiation complete.",
            "directive": (
                f"▶ INITIATE_PERSONA_INSTANTIATION({persona_name})\n"
                f"▶ Load ADAPTIVE_HANDOVER_BUNDLE:\n"
                f"  - Seeds: {', '.join(self._active_bundle['seeds']) if self._active_bundle else 'None'}\n"
                f"  - Overlay: {self._active_bundle['overlay_name'] if self._active_bundle else 'NOMINAL'}\n"
                f"  - Drift Level: {self._active_bundle['drift_level'] if self._active_bundle else 'N/A'}"
            ),
        }

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def active_bundle(self) -> Optional[Dict[str, Any]]:
        return self._active_bundle

    def session_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._sessions[-limit:]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "total_sessions":  self._session_count,
            "active_bundle":   self._active_bundle,
            "session_history": self.session_history(5),
        }


# Module-level singleton
session_handover = SessionHandover()
