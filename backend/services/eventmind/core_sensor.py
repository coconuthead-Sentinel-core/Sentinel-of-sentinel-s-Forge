"""
Signal Sensor
Analyzes user inputs for emotional signals, contextual urgency,
and intent classification.
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
_INTENT_CATEGORIES = {
    "creative":    {"create", "build", "design", "make", "generate", "invent", "imagine"},
    "analytical":  {"analyze", "evaluate", "measure", "compare", "assess", "examine", "review"},
    "directive":   {"run", "execute", "deploy", "send", "push", "activate", "start", "stop"},
    "inquisitive": {"what", "how", "why", "when", "where", "explain", "define", "describe"},
    "connective":  {"integrate", "connect", "link", "bridge", "sync", "merge", "combine"},
}


class SignalSensor:
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

        # --- Intent Category Scan ---
        intent_scores: Dict[str, int] = {}
        for category, seed_words in _INTENT_CATEGORIES.items():
            hits = len(word_set & seed_words)
            if hits:
                intent_scores[category] = hits

        if intent_scores:
            intent_category = max(intent_scores, key=lambda k: intent_scores[k])
            intent_confidence = round(min(intent_scores[intent_category] / 3, 1.0), 4)
        else:
            intent_category = "general"
            intent_confidence = 0.1

        # --- Latent Reading ---
        latent = self._latent_reading(dominant_emotion, intent_category, urgency)

        return {
            "emotional_signals": signals,
            "dominant_emotion": dominant_emotion,
            "urgency_level": urgency,
            "intent_category": intent_category,
            "intent_confidence": intent_confidence,
            "latent_reading": latent,
        }

    def _latent_reading(self, emotion: str | None, intent: str, urgency: float) -> str:
        """Synthesize a single intent interpretation statement."""
        if urgency >= 0.8:
            return "HIGH URGENCY — prioritize immediate resolution."
        if emotion == "disorientation":
            return "User context is unclear — recalibration needed before generating a response."
        if emotion == "friction":
            return "Friction pattern detected — a processing blockage or blocker is present."
        if emotion == "activation" and intent == "creative":
            return "Creative intent detected — system is primed for generative output."
        if intent == "analytical":
            return "Structured analytical inquiry detected — pattern analysis mode active."
        if intent == "connective":
            return "Integration intent detected — system is building a cross-domain bridge."
        if emotion == "resonance":
            return "Positive sentiment detected — input is well-matched to active context."
        return "Signal received. Processing through standard cognitive pipeline."
