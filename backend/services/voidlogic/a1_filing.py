"""
A1 Filing System
Symbolic memory tagging, retrieval, and drift monitoring for VoidLogic.

Every thought, session, or symbolic payload that passes through the engine
is filed here with rich metadata. Over time the system watches for "drift" —
when a concept shifts its meaning, frequency, or connection pattern — and
flags it for review.

Filing structure:
    tag          — primary symbolic label (e.g. "recursion", "emergence")
    domain       — symbolic domain (logic / emotion / pattern / system / myth)
    confidence   — 0.0–1.0 certainty that the tag is accurate
    access_count — how many times this filing has been retrieved
    drift_score  — how much this filing has changed since first creation

Drift is computed as:
    Δconfidence + Δaccess_rate divergence from rolling mean
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional


_DOMAINS = {"logic", "emotion", "pattern", "system", "myth", "general"}
_DRIFT_THRESHOLD = 0.35     # above this → filing is marked DRIFTED
_MAX_FILINGS = 2000


class A1Filing:
    """A single filed symbolic memory."""

    def __init__(
        self,
        content: str,
        tag: str,
        domain: str = "general",
        confidence: float = 0.8,
    ) -> None:
        self.id           = str(uuid.uuid4())[:10]
        self.content      = content
        self.tag          = tag.lower().strip()
        self.domain       = domain if domain in _DOMAINS else "general"
        self.confidence   = round(min(max(confidence, 0.0), 1.0), 4)
        self.access_count = 0
        self.created_at   = time.time()
        self.updated_at   = time.time()

        # Drift tracking
        self._initial_confidence = self.confidence
        self._access_timestamps: List[float] = []
        self.drift_score  = 0.0
        self.drift_status = "STABLE"

    def access(self) -> None:
        now = time.time()
        self.access_count += 1
        self._access_timestamps.append(now)
        self.updated_at = now
        self._recompute_drift()

    def update_confidence(self, new_confidence: float) -> None:
        self.confidence = round(min(max(new_confidence, 0.0), 1.0), 4)
        self.updated_at = time.time()
        self._recompute_drift()

    def _recompute_drift(self) -> None:
        confidence_delta = abs(self.confidence - self._initial_confidence)

        # Access rate divergence: compare recent vs historical rate
        if len(self._access_timestamps) >= 4:
            half = len(self._access_timestamps) // 2
            early = self._access_timestamps[:half]
            recent = self._access_timestamps[half:]
            early_rate  = (half) / max(early[-1] - early[0], 1)
            recent_rate = (len(recent)) / max(recent[-1] - recent[0], 1)
            rate_delta = min(abs(recent_rate - early_rate) / max(early_rate, 0.001), 1.0)
        else:
            rate_delta = 0.0

        self.drift_score  = round(min((confidence_delta * 0.6) + (rate_delta * 0.4), 1.0), 4)
        self.drift_status = "DRIFTED" if self.drift_score >= _DRIFT_THRESHOLD else "STABLE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "tag":          self.tag,
            "domain":       self.domain,
            "confidence":   self.confidence,
            "access_count": self.access_count,
            "drift_score":  self.drift_score,
            "drift_status": self.drift_status,
            "created_at":   round(self.created_at, 3),
            "updated_at":   round(self.updated_at, 3),
            "content":      self.content[:200],   # truncate for snapshot
        }


class A1FilingSystem:
    """
    The A1 Filing System — master symbolic memory index for VoidLogic.
    Files thoughts, monitors drift, and supports tag/domain retrieval.
    """

    def __init__(self) -> None:
        self._filings: Dict[str, A1Filing] = {}        # id → filing
        self._tag_index: Dict[str, List[str]] = {}     # tag → [ids]
        self._domain_index: Dict[str, List[str]] = {}  # domain → [ids]
        self._total_filed = 0
        self._drift_alerts: List[Dict[str, Any]] = []  # last 100 drift events

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def file(
        self,
        content: str,
        tag: str,
        domain: str = "general",
        confidence: float = 0.8,
    ) -> Dict[str, Any]:
        """File a new symbolic memory."""
        # Enforce capacity
        if len(self._filings) >= _MAX_FILINGS:
            self._evict_lowest_confidence()

        f = A1Filing(content, tag, domain, confidence)
        self._filings[f.id] = f

        self._tag_index.setdefault(f.tag, []).append(f.id)
        self._domain_index.setdefault(f.domain, []).append(f.id)
        self._total_filed += 1

        return {
            "filing_id":    f.id,
            "tag":          f.tag,
            "domain":       f.domain,
            "confidence":   f.confidence,
            "total_filed":  self._total_filed,
        }

    def retrieve_by_tag(self, tag: str, limit: int = 10) -> List[Dict[str, Any]]:
        ids = self._tag_index.get(tag.lower().strip(), [])
        results = []
        for fid in ids[-limit:]:
            if fid in self._filings:
                f = self._filings[fid]
                f.access()
                if f.drift_status == "DRIFTED":
                    self._log_drift(f)
                results.append(f.to_dict())
        return results

    def retrieve_by_domain(self, domain: str, limit: int = 20) -> List[Dict[str, Any]]:
        ids = self._domain_index.get(domain, [])
        results = []
        for fid in ids[-limit:]:
            if fid in self._filings:
                f = self._filings[fid]
                f.access()
                results.append(f.to_dict())
        return results

    def drift_report(self) -> Dict[str, Any]:
        """Full drift analysis across all filings."""
        drifted = [f.to_dict() for f in self._filings.values() if f.drift_status == "DRIFTED"]
        avg_drift = (
            round(sum(f.drift_score for f in self._filings.values()) / len(self._filings), 4)
            if self._filings else 0.0
        )
        return {
            "total_filings":    len(self._filings),
            "drifted_count":    len(drifted),
            "avg_drift_score":  avg_drift,
            "system_status":    "DRIFTING" if len(drifted) > len(self._filings) * 0.2 else "STABLE",
            "drifted_filings":  drifted[:20],
            "recent_alerts":    self._drift_alerts[-10:],
        }

    def index_snapshot(self) -> Dict[str, Any]:
        return {
            "total_filings":   len(self._filings),
            "total_tags":      len(self._tag_index),
            "total_domains":   len(self._domain_index),
            "domain_counts":   {d: len(ids) for d, ids in self._domain_index.items()},
            "tag_counts":      {t: len(ids) for t, ids in self._tag_index.items()},
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _evict_lowest_confidence(self) -> None:
        if not self._filings:
            return
        victim_id = min(self._filings, key=lambda fid: self._filings[fid].confidence)
        f = self._filings.pop(victim_id)
        # Remove from indices
        if f.tag in self._tag_index:
            self._tag_index[f.tag] = [i for i in self._tag_index[f.tag] if i != victim_id]
        if f.domain in self._domain_index:
            self._domain_index[f.domain] = [i for i in self._domain_index[f.domain] if i != victim_id]

    def _log_drift(self, f: A1Filing) -> None:
        self._drift_alerts = (self._drift_alerts + [{
            "filing_id":   f.id,
            "tag":         f.tag,
            "drift_score": f.drift_score,
            "timestamp":   round(time.time(), 3),
        }])[-100:]


# Module-level singleton
a1 = A1FilingSystem()
