"""
Multi-Perspective Analyzer
Processes user input through three independent scoring vectors:

    1. Intent Weight    — the purpose density of the input (action words, questions)
    2. Context Vector   — the situational domain (technical, conceptual, emotional)
    3. Structural Match — input structure score (punctuation, length, specificity)

Returns a composite score and per-vector breakdown.
"""
from __future__ import annotations

import re
from typing import Dict, Any, List


# --- Intent Weight Analysis ---
_ACTION_WORDS = {
    "build", "create", "make", "design", "write", "generate", "produce",
    "solve", "fix", "analyze", "explain", "find", "show", "tell", "help",
    "optimize", "improve", "deploy", "integrate", "connect", "run", "start",
}

_QUESTION_MARKERS = {"what", "how", "why", "when", "where", "who", "which", "can", "could", "would", "should"}

# --- Context Vector Analysis ---
_TECHNICAL_CONTEXT = {
    "api", "code", "python", "server", "database", "endpoint", "function",
    "module", "class", "docker", "git", "deploy", "backend", "frontend",
    "ai", "model", "data", "system", "architecture", "protocol",
}

_CONCEPTUAL_CONTEXT = {
    "idea", "concept", "theory", "framework", "philosophy", "vision",
    "strategy", "approach", "principle", "model", "design", "pattern",
}

_EMOTIONAL_CONTEXT = {
    "feel", "want", "need", "hope", "worry", "fear", "excited", "confused",
    "frustrated", "happy", "grateful", "struggle", "overwhelmed",
}


class MultiPerspectiveAnalyzer:
    """
    Three-vector input analyzer for EventMind.
    Each vector returns a score 0.0–1.0 and a classification label.
    """

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Run all three vectors against the input text.

        Returns:
            {
                intent_weight: {score, label, indicators},
                context_vector: {score, label, domain},
                frequency_match: {score, label},
                triangulated_score: float,
                signal_class: str
            }
        """
        words_raw = text.lower().split()
        words = set(words_raw)
        word_count = max(len(words_raw), 1)

        intent = self._intent_weight(words, word_count, text)
        context = self._context_vector(words)
        structure = self._structural_match(text, word_count)

        # Weighted score: intent carries most weight
        tri_score = round(
            (intent["score"] * 0.45) +
            (context["score"] * 0.30) +
            (structure["score"] * 0.25),
            4
        )

        signal_class = (
            "APEX"     if tri_score >= 0.75 else
            "STRONG"   if tri_score >= 0.55 else
            "MODERATE" if tri_score >= 0.35 else
            "WEAK"
        )

        return {
            "intent_weight": intent,
            "context_vector": context,
            "structural_match": structure,
            "triangulated_score": tri_score,
            "signal_class": signal_class,
        }

    def _intent_weight(self, words: set, word_count: int, text: str) -> Dict[str, Any]:
        action_hits = list(words & _ACTION_WORDS)
        question_hits = list(words & _QUESTION_MARKERS)
        sentence_count = max(len(re.split(r'[.!?]', text)), 1)

        # Dense, purposeful inputs score higher
        density = min((len(action_hits) * 2 + len(question_hits)) / word_count * 5, 1.0)
        complexity = min(sentence_count / 5, 1.0)
        score = round((density * 0.7) + (complexity * 0.3), 4)

        label = (
            "HIGH_GRAVITY"  if score >= 0.65 else
            "MID_ORBIT"     if score >= 0.35 else
            "LOW_PULL"
        )

        return {
            "score": score,
            "label": label,
            "action_indicators": action_hits,
            "question_markers": question_hits,
        }

    def _context_vector(self, words: set) -> Dict[str, Any]:
        tech_hits = list(words & _TECHNICAL_CONTEXT)
        concept_hits = list(words & _CONCEPTUAL_CONTEXT)
        emotion_hits = list(words & _EMOTIONAL_CONTEXT)

        counts = {
            "technical":   len(tech_hits),
            "conceptual":  len(concept_hits),
            "emotional":   len(emotion_hits),
        }
        dominant = max(counts, key=lambda k: counts[k])
        total_hits = sum(counts.values())
        score = round(min(total_hits / 4, 1.0), 4)

        return {
            "score": score,
            "label": f"VECTOR_{dominant.upper()}",
            "domain": dominant,
            "technical_hits": tech_hits,
            "conceptual_hits": concept_hits,
            "emotional_hits": emotion_hits,
        }

    def _structural_match(self, text: str, word_count: int) -> Dict[str, Any]:
        # Structural match: longer, well-punctuated, specific inputs score higher
        punct_count = len(re.findall(r'[,;:\-–—]', text))
        caps_count = len(re.findall(r'\b[A-Z]{2,}\b', text))
        number_count = len(re.findall(r'\b\d+\b', text))

        score = round(min(
            (punct_count * 0.1) +
            (caps_count * 0.15) +
            (number_count * 0.05) +
            (min(word_count, 50) / 50 * 0.5),
            1.0
        ), 4)

        label = (
            "IN_SYNC"      if score >= 0.6 else
            "NEAR_SYNC"    if score >= 0.35 else
            "OUT_OF_PHASE"
        )

        return {"score": score, "label": label}
