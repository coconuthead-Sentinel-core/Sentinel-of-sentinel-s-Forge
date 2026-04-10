"""
Core Sensor
Analyzes user inputs for emotional signals, contextual urgency,
and vibrational intent — the latent meaning beneath the surface words.
"""
from __future__ import annotations

from typing import Dict, Any, List


# Emotional signal map: word → (emotion_label, intensity 0.0-1.0)
_EMOTIONAL_SIGNALS: Dict[str, tuple] = {
    # High intensity
    "urgent":      ("urgency",     0.9),
    "critical":    ("urgency",     0.95),
    "emergency":   ("urgency",     1.0),
    "broken":      ("distress",    0.85),
    "failed":      ("distress",    0.8),
    "lost":        ("disorientation", 0.75),
    "confused":    ("disorientation", 0.7),
    "frustrated":  ("friction",    0.8),
    "stuck":       ("friction",    0.75),
    "overwhelmed": ("overload",    0.9),
    # Positive signals
    "excited":     ("activation",  0.85),
    "ready":       ("activation",  0.7),
    "curious":     ("inquiry",     0.65),
    "interested":  ("inquiry",     0.6),
    "love":        ("resonance",   0.8),
    "great":       ("resonance",   0.6),
    "perfect":     ("resonance",   0.75),
    # Neutral but weighted
    "need":        ("necessity",   0.7),
    "must":        ("necessity",   0.8),
    "important":   ("priority",    0.7),
    "help":        ("dependency",  0.65),
    "please":      ("courtesy",    0.4),
    "thank":       ("gratitude",   0.5),
}

# Vibrational intent categories
_INTENT_VIBRATIONS = {
    "creative":    {"create", "build", "design", "make", "generate", "invent", "imagine"},
    "analytical":  {"analyze", "evaluate", "measure", "compare", "assess", "examine", "review"},
    "directive":   {"run", "execute", "deploy", "send", "push", "activate", "start", "stop"},
    "inquisitive": {"what", "how", "why", "when", "where", "explain", "define", "describe"},
    "connective":  {"integrate", "connect", "link", "bridge", "sync", "merge", "combine"},
}


class CoreSensor:
    """
    Reads emotional charge, urgency level, and vibrational intent
    from raw input text.
    """

    def sense(self, text: str) -> Dict[str, Any]:
        """
        Analyze the input for emotional and vibrational signals.

        Returns:
            {
                emotional_signals: [{emotion, word, intensity}],
                dominant_emotion: str | None,
                urgency_level: float,
                vibrational_intent: str,
                intent_confidence: float,
                latent_reading: str
            }
        """
        words = [w.strip(".,!?;:").lower() for w in text.split()]
        word_set = set(words)

        # --- Emotional Scan ---
        signals: List[Dict[str, Any]] = []
        for word in words:
            if word in _EMOTIONAL_SIGNALS:
                emotion, intensity = _EMOTIONAL_SIGNALS[word]
                signals.append({"emotion": emotion, "word": word, "intensity": intensity})

        dominant_emotion = None
        urgency = 0.0
        if signals:
            # Dominant = highest intensity signal
            top = max(signals, key=lambda s: s["intensity"])
            dominant_emotion = top["emotion"]
            urgency = round(max(s["intensity"] for s in signals if s["emotion"] == "urgency") if
                            any(s["emotion"] == "urgency" for s in signals) else 0.0, 4)

        # --- Vibrational Intent Scan ---
        vib_scores: Dict[str, int] = {}
        for vib, seed_words in _INTENT_VIBRATIONS.items():
            hits = len(word_set & seed_words)
            if hits:
                vib_scores[vib] = hits

        if vib_scores:
            vibrational_intent = max(vib_scores, key=lambda k: vib_scores[k])
            intent_confidence = round(min(vib_scores[vibrational_intent] / 3, 1.0), 4)
        else:
            vibrational_intent = "ambient"
            intent_confidence = 0.1

        # --- Latent Reading ---
        latent = self._latent_reading(dominant_emotion, vibrational_intent, urgency)

        return {
            "emotional_signals": signals,
            "dominant_emotion": dominant_emotion,
            "urgency_level": urgency,
            "vibrational_intent": vibrational_intent,
            "intent_confidence": intent_confidence,
            "latent_reading": latent,
        }

    def _latent_reading(self, emotion: str | None, intent: str, urgency: float) -> str:
        """Synthesize a single latent interpretation statement."""
        if urgency >= 0.8:
            return "HIGH URGENCY FIELD DETECTED — prioritise immediate resolution pathway."
        if emotion == "disorientation":
            return "The signal carries navigational drift — recalibration of context is needed."
        if emotion == "friction":
            return "Resistance pattern detected — a blockage in the processing flow is present."
        if emotion == "activation" and intent == "creative":
            return "Generative resonance is high — the system is primed for creative output."
        if intent == "analytical":
            return "Structured inquiry detected — deep pattern analysis mode engaged."
        if intent == "connective":
            return "Integration intent active — bridge-building sequence initialised."
        if emotion == "resonance":
            return "Positive frequency alignment — the signal is well-matched to the system pulse."
        return "Signal received. Processing through standard cognitive pathways."
