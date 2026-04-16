"""
Cross-Domain Knowledge Bridge
Connective reasoning layer for the SymbolicReasoningEngine.

A KnowledgeBridgeThread is a live link between two cognitive domains
(e.g. logic ↔ emotion, pattern ↔ system) that carries a translation layer —
a set of mappings that let a concept from one domain be interpreted
and operated on within another.

Threads are created on demand, strengthened by use, and pruned when inactive.

Architecture:
    KnowledgeBridgeThread  — directed domain-to-domain link with translation table
    CrossDomainBridgeWeaver — orchestrator: creates, reinforces, and prunes threads
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional, Tuple


# Domain translation tables: source → target concept mappings
_DOMAIN_BRIDGE_TEMPLATES: Dict[Tuple[str, str], List[str]] = {
    ("logic",   "emotion"):  ["certainty→conviction", "error→confusion", "loop→fixation", "proof→trust"],
    ("logic",   "pattern"):  ["axiom→seed", "theorem→template", "if-then→trigger", "variable→node"],
    ("logic",   "narrative"):["theorem→rule", "axiom→principle", "contradiction→conflict", "proof→resolution"],
    ("emotion", "pattern"):  ["intensity→amplitude", "mood→baseline", "shift→transition", "urgency→spike"],
    ("emotion", "system"):   ["urgency→priority", "confidence→weight", "hesitation→delay", "focus→lock"],
    ("pattern", "system"):   ["cycle→loop", "signal→event", "recursion→recursive_call", "seed→init_state"],
    ("pattern", "narrative"):["cycle→arc", "signal→indicator", "recursion→callback", "emergence→development"],
    ("system",  "narrative"):["process→workflow", "failure→blocker", "restart→recovery", "overflow→saturation"],
}

_DECAY_RATE     = 0.02     # weight lost per access cycle if not reinforced
_REINFORCE_RATE = 0.05     # weight gained per use
_MIN_WEIGHT     = 0.1      # below this the thread is pruned
_MAX_THREADS    = 200


class KnowledgeBridgeThread:
    """A single directed cross-domain knowledge bridge."""

    def __init__(self, source: str, target: str) -> None:
        self.id            = str(uuid.uuid4())[:8]
        self.source        = source
        self.target        = target
        self.weight        = 0.5
        self.created_at    = time.time()
        self.last_used     = time.time()
        self.use_count     = 0
        self.translations: List[str] = self._load_translations()
        self.active        = True

    def _load_translations(self) -> List[str]:
        key = (self.source, self.target)
        alt = (self.target, self.source)
        return (
            _DOMAIN_BRIDGE_TEMPLATES.get(key, []) or
            _DOMAIN_BRIDGE_TEMPLATES.get(alt, []) or
            [f"{self.source}↔{self.target} (direct link)"]
        )

    def use(self) -> "KnowledgeBridgeThread":
        self.use_count += 1
        self.last_used  = time.time()
        self.weight     = round(min(self.weight + _REINFORCE_RATE, 1.0), 4)
        return self

    def decay(self) -> None:
        if self.use_count == 0 or (time.time() - self.last_used) > 300:
            self.weight = round(max(self.weight - _DECAY_RATE, 0.0), 4)
        if self.weight <= _MIN_WEIGHT:
            self.active = False

    def translate(self, concept: str) -> str:
        """Attempt to translate a concept across the bridge."""
        concept_lower = concept.lower()
        for t in self.translations:
            parts = t.replace("↔", "→").split("→")
            if len(parts) == 2:
                src_word, tgt_word = parts[0].strip(), parts[1].strip()
                if src_word in concept_lower:
                    return concept_lower.replace(src_word, tgt_word)
        return f"[{self.target}::{concept}]"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "source":       self.source,
            "target":       self.target,
            "weight":       self.weight,
            "use_count":    self.use_count,
            "translations": self.translations,
            "active":       self.active,
            "last_used":    round(self.last_used, 3),
        }


class CrossDomainBridgeWeaver:
    """
    Orchestrates cross-domain knowledge bridge threads.
    Creates bridges on demand, reinforces used bridges, prunes inactive ones.
    """

    def __init__(self) -> None:
        self._threads: Dict[str, KnowledgeBridgeThread] = {}
        self._index: Dict[Tuple[str, str], str] = {}   # (src, tgt) → thread id
        self._total_translations = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def bridge(self, source: str, target: str) -> Dict[str, Any]:
        """Get or create a bridge thread between source and target domains."""
        key = (source, target)
        alt = (target, source)

        thread_id = self._index.get(key) or self._index.get(alt)
        if thread_id and thread_id in self._threads:
            thread = self._threads[thread_id].use()
        else:
            if len(self._threads) >= _MAX_THREADS:
                self._prune()
            thread = KnowledgeBridgeThread(source, target)
            self._threads[thread.id] = thread
            self._index[key] = thread.id

        return {
            "thread_id":    thread.id,
            "source":       thread.source,
            "target":       thread.target,
            "weight":       thread.weight,
            "translations": thread.translations,
            "use_count":    thread.use_count,
        }

    def translate(self, concept: str, source: str, target: str) -> Dict[str, Any]:
        """Translate a concept from source domain to target domain."""
        bridge_info = self.bridge(source, target)
        thread_id   = bridge_info["thread_id"]
        thread      = self._threads[thread_id]
        translated  = thread.translate(concept)
        self._total_translations += 1

        return {
            "original":      concept,
            "translated":    translated,
            "source":        source,
            "target":        target,
            "thread_id":     thread_id,
            "bridge_weight": thread.weight,
        }

    def cross_domain_insight(self, concept: str, source: str) -> List[Dict[str, Any]]:
        """
        Translate a concept from the source domain into all other known domains.
        """
        known_domains = {"logic", "emotion", "pattern", "system", "narrative", "general"}
        others = known_domains - {source}
        return [self.translate(concept, source, tgt) for tgt in others]

    def active_threads(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._threads.values() if t.active]

    def weave_snapshot(self) -> Dict[str, Any]:
        active = [t for t in self._threads.values() if t.active]
        return {
            "total_threads":      len(self._threads),
            "active_threads":     len(active),
            "total_translations": self._total_translations,
            "strongest_bridge":   max(active, key=lambda t: t.weight).to_dict() if active else None,
            "weakest_bridge":     min(active, key=lambda t: t.weight).to_dict() if active else None,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _prune(self) -> None:
        """Decay all threads and remove inactive ones."""
        dead = []
        for thread in self._threads.values():
            thread.decay()
            if not thread.active:
                dead.append(thread.id)
        for tid in dead:
            t = self._threads.pop(tid)
            key = (t.source, t.target)
            self._index.pop(key, None)


# Module-level singleton
knowledge_bridge = CrossDomainBridgeWeaver()
