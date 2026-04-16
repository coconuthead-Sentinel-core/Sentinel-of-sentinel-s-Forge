"""
Output Tagging System
Structured metadata tagging for all SymbolicReasoningEngine outputs.

Implements a structured tag format for audit and traceability:
    [TagType_YYYY-MM-DD-HH-MM_Summary_Status].Type

Tag Types:
    NodePrimary    — Root activation node for a session or pipeline
    Synthesis      — Multi-modal cognitive merge or lens combination
    Anchor         — System activation confirmation / ground-truth stamp
    OutputDoc      — Formatted AI output or documentation artifact
    CommentSection — Reflective dialog or annotation
    Directive      — Next-step action or instruction block
    Regulation     — Compliance, risk, or governance notice

Status Values:
    GREEN  — Active, healthy, fully operational
    YELLOW — Warning, partial activation, review needed
    RED    — Blocked, failed, or governance violation
"""
from __future__ import annotations

import re
import time
import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TAG_TYPES = {
    "NodePrimary":    "Root activation node — marks session or pipeline entry",
    "Synthesis":      "Multi-modal cognitive merge or lens combination result",
    "Anchor":         "System activation confirmation / ground-truth stamp",
    "OutputDoc":      "Formatted AI output or documentation artifact",
    "CommentSection": "Reflective dialog or mentored annotation",
    "Directive":      "Next-step action or instruction block",
    "Regulation":     "Compliance, risk, or governance notice",
}

_STATUS_THRESHOLDS = {
    "GREEN":  "Active, healthy, fully operational",
    "YELLOW": "Warning, partial activation, review needed",
    "RED":    "Blocked, failed, or governance violation",
}

_TAG_PATTERN = re.compile(
    r"\[(?P<tag_type>\w+)_(?P<date>\d{4}-\d{2}-\d{2}(-\d{2}-\d{2})?)_"
    r"(?P<summary>[^_]+)_(?P<status>GREEN|YELLOW|RED)\]\.Type",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Core tag builder
# ---------------------------------------------------------------------------

def _now_stamp() -> str:
    """Return YYYY-MM-DD-HH-MM timestamp in local time."""
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")


def _infer_status(score: float) -> str:
    """Map a 0–1 score to GREEN / YELLOW / RED."""
    if score >= 0.65:
        return "GREEN"
    elif score >= 0.35:
        return "YELLOW"
    return "RED"


def build_tag(
    tag_type: str,
    summary: str,
    status: Optional[str] = None,
    score: Optional[float] = None,
) -> str:
    """
    Build a canonical Nexus tag string.

    Args:
        tag_type: One of the TAG_TYPES keys (case-insensitive, defaults to OutputDoc).
        summary:  Short snake_case label describing the content.
        status:   Explicit GREEN / YELLOW / RED (overrides score).
        score:    0–1 float used to infer status if status is None.

    Returns:
        e.g. "[OutputDoc_2025-06-22-14-30_EmergenceDetected_GREEN].Type"
    """
    ttype = tag_type if tag_type in TAG_TYPES else "OutputDoc"
    safe_summary = re.sub(r"[^a-zA-Z0-9_]", "_", summary.strip())[:40]
    st = status or (score is not None and _infer_status(score)) or "GREEN"
    stamp = _now_stamp()
    return f"[{ttype}_{stamp}_{safe_summary}_{st}].Type"


def parse_tag(tag_string: str) -> Optional[Dict[str, str]]:
    """Parse a Nexus tag string back into its components."""
    m = _TAG_PATTERN.search(tag_string)
    if not m:
        return None
    return {
        "tag_type": m.group("tag_type"),
        "date":     m.group("date"),
        "summary":  m.group("summary"),
        "status":   m.group("status"),
        "raw":      m.group(0),
    }


# ---------------------------------------------------------------------------
# OutputTaggingSystem class
# ---------------------------------------------------------------------------

class OutputTaggingSystem:
    """
    Central tag registry for all VoidLogic outputs.
    Tags are stored with their payload for later recall and audit.
    """

    def __init__(self) -> None:
        self._registry: List[Dict[str, Any]] = []   # chronological log
        self._total = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def tag(
        self,
        payload: Any,
        tag_type: str = "OutputDoc",
        summary: str = "VoidLogicOutput",
        status: Optional[str] = None,
        score: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Tag a payload and store it in the registry.

        Args:
            payload:   The content being tagged (string, dict, etc.)
            tag_type:  Nexus tag type.
            summary:   Short descriptor for the tag summary field.
            status:    Explicit GREEN/YELLOW/RED.
            score:     0–1 health/quality score (used if status is None).

        Returns:
            Dict with 'tag', 'payload', 'stored_at', 'registry_index'.
        """
        tag_str = build_tag(tag_type, summary, status=status, score=score)
        entry = {
            "tag":            tag_str,
            "tag_type":       tag_type if tag_type in TAG_TYPES else "OutputDoc",
            "summary":        summary,
            "status":         status or (score is not None and _infer_status(score)) or "GREEN",
            "payload":        payload,
            "stored_at":      round(time.time(), 3),
            "registry_index": self._total,
        }
        self._registry.append(entry)
        self._total += 1
        return entry

    def auto_tag(self, voidlogic_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically select tag type and status from a VoidLogic engine result.
        Attaches the tag to the result dict in-place and returns it.
        """
        health = voidlogic_result.get("reasoning_report", {}).get("system_health", "NOMINAL")
        crfe   = voidlogic_result.get("reasoning_report", {}).get("crfe", {})

        # Determine tag type from health
        tag_type = {
            "CRITICAL":  "Regulation",
            "AMPLIFIED": "NodePrimary",
            "EMERGING":  "Synthesis",
            "NOMINAL":   "OutputDoc",
        }.get(health, "OutputDoc")

        # Determine status from system health
        status = {
            "CRITICAL":  "RED",
            "AMPLIFIED": "GREEN",
            "EMERGING":  "GREEN",
            "NOMINAL":   "GREEN",
        }.get(health, "YELLOW")

        # Build summary from dominant signal
        emergence = crfe.get("emergence", {})
        rsml      = crfe.get("rsml", {})
        summary = (
            emergence.get("emergent_pattern") or
            (rsml.get("matched_markers") or ["NoSignal"])[0] or
            health
        )

        entry = self.tag(
            payload  = voidlogic_result,
            tag_type = tag_type,
            summary  = str(summary)[:40],
            status   = status,
        )
        voidlogic_result["nexus_tag"] = entry["tag"]
        return voidlogic_result

    def tag_ai_response(
        self,
        response_text: str,
        lens: str = "neurotypical",
        latency_ms: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Tag a raw AI response text with OutputDoc metadata.
        Used by the cognitive orchestrator to stamp every response.
        """
        score = max(0.0, 1.0 - (latency_ms / 10000))  # faster = healthier
        summary = f"{lens}_response"
        return self.tag(
            payload  = response_text,
            tag_type = "OutputDoc",
            summary  = summary,
            score    = score,
        )

    def recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return the most recent tagged entries."""
        return self._registry[-limit:]

    def by_status(self, status: str) -> List[Dict[str, Any]]:
        """Return all entries with a given status."""
        return [e for e in self._registry if e["status"] == status.upper()]

    def by_type(self, tag_type: str) -> List[Dict[str, Any]]:
        """Return all entries of a given tag type."""
        return [e for e in self._registry if e["tag_type"] == tag_type]

    def registry_snapshot(self) -> Dict[str, Any]:
        """Summary statistics of the tag registry."""
        status_counts: Dict[str, int] = {}
        type_counts:   Dict[str, int] = {}
        for e in self._registry:
            status_counts[e["status"]]   = status_counts.get(e["status"], 0) + 1
            type_counts[e["tag_type"]]   = type_counts.get(e["tag_type"], 0) + 1
        return {
            "total_tags":     self._total,
            "status_counts":  status_counts,
            "type_counts":    type_counts,
            "tag_types":      TAG_TYPES,
            "status_values":  _STATUS_THRESHOLDS,
        }


# Module-level singleton
nexus_tag = OutputTaggingSystem()
