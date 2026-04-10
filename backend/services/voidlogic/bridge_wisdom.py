"""
Bridge Wisdom Threads (BWT)
Trans-domain connective tissue for VoidLogic.

A Bridge Wisdom Thread is a live symbolic link between two domains
(e.g. logic ↔ emotion, pattern ↔ myth) that carries a "translation layer" —
a set of mappings that let a concept from one domain be understood
and operated on within another.

Threads are created on demand, strengthened by use, and decay if unused.
The BWT module enables VoidLogic to reason across domain boundaries
without losing the unique properties of each domain.

Architecture:
    Thread:  source_domain → target_domain, weight (0–1), active translations
    Bridge:  a named two-way thread with bidirectional translation tables
    Weaver:  orchestrator that creates, strengthens, and prunes threads
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any, List, Optional, Tuple


# Default domain translation templates
_DOMAIN_BRIDGE_TEMPLATES: Dict[Tuple[str, str], List[str]] = {
    ("logic",   "emotion"):  ["certainty→conviction", "error→confusion", "loop→obsession", "proof→trust"],
    ("logic",   "pattern"):  ["axiom→seed", "theorem→fractal", "if-then→trigger", "variable→node"],
    ("logic",   "myth"):     ["theorem→prophecy", "axiom→law", "contradiction→paradox", "proof→revelation"],
    ("emotion", "pattern"):  ["feeling→signal", "intensity→amplitude", "mood→frequency", "shift→transition"],
    ("emotion", "system"):   ["urgency→priority", "fear→risk_flag", "confidence→weight", "hesitation→delay"],
    ("pattern", "system"):   ["fractal→recursive_call", "signal→event", "echo→feedback", "seed→init_state"],
    ("pattern", "myth"):     ["cycle→eternal_return", "echo→reverberation", "emergence→awakening", "signal→omen"],
    ("system",  "myth"):     ["process→ritual", "failure→trial", "restart→rebirth", "overflow→flood"],
}

_DECAY_RATE = 0.02         # weight lost per access cycle if not reinforced
_REINFORCE_RATE = 0.05     # weight gained per use
_MIN_WEIGHT = 0.1          # below this the thread is pruned
_MAX_THREADS = 200


class WisdomThread:
    """A single trans-domain bridge thread."""

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
            [f"{self.source}↔{self.target} (raw symbolic link)"]
        )

    def use(self) -> "WisdomThread":
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


class BridgeWisdomWeaver:
    """
    Orchestrates trans-domain wisdom threads.
    Creates bridges on demand, reinforces used bridges, prunes dead ones.
    """

    def __init__(self) -> None:
        self._threads: Dict[str, WisdomThread] = {}   # id → thread
        self._index: Dict[Tuple[str, str], str] = {}  # (src, tgt) → thread id
        self._total_translations = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def bridge(self, source: str, target: str) -> Dict[str, Any]:
        """Get or create a thread between source and target domains."""
        key = (source, target)
        alt = (target, source)

        thread_id = self._index.get(key) or self._index.get(alt)
        if thread_id and thread_id in self._threads:
            thread = self._threads[thread_id].use()
        else:
            if len(self._threads) >= _MAX_THREADS:
                self._prune()
            thread = WisdomThread(source, target)
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
            "original":    concept,
            "translated":  translated,
            "source":      source,
            "target":      target,
            "thread_id":   thread_id,
            "bridge_weight": thread.weight,
        }

    def cross_domain_insight(self, concept: str, source: str) -> List[Dict[str, Any]]:
        """
        Translate a concept from source domain into ALL other known domains
        simultaneously — the VoidLogic "prismatic view."
        """
        known_domains = {"logic", "emotion", "pattern", "system", "myth", "general"}
        others = known_domains - {source}
        return [self.translate(concept, source, tgt) for tgt in others]

    def active_threads(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self._threads.values() if t.active]

    def weave_snapshot(self) -> Dict[str, Any]:
        active = [t for t in self._threads.values() if t.active]
        return {
            "total_threads":       len(self._threads),
            "active_threads":      len(active),
            "total_translations":  self._total_translations,
            "strongest_bridge":    max(active, key=lambda t: t.weight).to_dict() if active else None,
            "weakest_bridge":      min(active, key=lambda t: t.weight).to_dict() if active else None,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _prune(self) -> None:
        """Decay all threads and remove dead ones."""
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
bwt = BridgeWisdomWeaver()
