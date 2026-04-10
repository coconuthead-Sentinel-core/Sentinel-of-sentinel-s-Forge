"""
Core Pulse Engine
The heartbeat of EventMind. Generates an internal frequency signature and
measures how strongly an incoming input resonates with it.

When resonance is HIGH  → full processing activated
When resonance is LOW   → returns a "gravitational hum" (minimal, ambient response)
"""
from __future__ import annotations

import hashlib
import math
import time
from typing import Dict, Any


# Base frequency keywords — inputs containing these resonate strongly
_HIGH_RESONANCE_SEEDS = {
    "gravity", "frequency", "resonance", "cognition", "intelligence",
    "pattern", "signal", "wave", "field", "consciousness", "quantum",
    "vector", "node", "memory", "synthesis", "emergence", "flux",
    "nexus", "sentinel", "core", "pulse", "data", "system", "mind",
    "analysis", "process", "learn", "adapt", "evolve", "create",
    "build", "design", "architect", "solve", "optimize", "generate",
}

_SILENCE_THRESHOLD = 0.25   # below this → gravitational hum
_FULL_THRESHOLD    = 0.55   # above this → full resonance


class CorePulse:
    """
    Measures frequency resonance between the system's internal pulse
    and an incoming user input.
    """

    def __init__(self) -> None:
        # Generate a time-seeded internal pulse signature
        self._pulse_seed = self._generate_pulse()

    def _generate_pulse(self) -> float:
        """Create a deterministic but session-unique pulse value 0.0–1.0."""
        raw = hashlib.sha256(str(time.time()).encode()).hexdigest()
        return int(raw[:8], 16) / 0xFFFFFFFF

    def measure(self, text: str) -> Dict[str, Any]:
        """
        Measure resonance of input text against the Core Pulse.

        Returns:
            {
                score: float (0.0–1.0),
                state: "full" | "partial" | "silent",
                matched_seeds: [str],
                hum: str | None   — ambient response if silent
            }
        """
        words = set(text.lower().split())
        matched = list(words & _HIGH_RESONANCE_SEEDS)

        # Base score: ratio of matched seeds
        seed_score = min(len(matched) / max(len(words), 1) * 3.0, 1.0)

        # Modulate by pulse (adds subtle session variation)
        score = round((seed_score * 0.8) + (self._pulse_seed * 0.2), 4)
        score = min(score, 1.0)

        if score >= _FULL_THRESHOLD:
            state = "full"
            hum = None
        elif score >= _SILENCE_THRESHOLD:
            state = "partial"
            hum = None
        else:
            state = "silent"
            hum = self._gravitational_hum(text)

        return {
            "score": score,
            "state": state,
            "matched_seeds": matched,
            "hum": hum,
            "pulse_signature": round(self._pulse_seed, 6),
        }

    def _gravitational_hum(self, text: str) -> str:
        """Generate an ambient, enigmatic response for low-resonance inputs."""
        hums = [
            "~ The signal is weak. What lies beneath the surface of your question?",
            "~ A faint gravitational echo. Refine the frequency of your inquiry.",
            "~ The event horizon absorbs this. Ask from a deeper orbit.",
            "~ Insufficient resonance detected. What is the true mass of your query?",
            "~ The pulse does not recognise this wavelength. Restate with intent.",
        ]
        idx = int(hashlib.md5(text.encode()).hexdigest(), 16) % len(hums)
        return hums[idx]
