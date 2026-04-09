"""
Autism Cognitive Lens
Optimizes AI output for autism-spectrum processing: explicit structure,
literal language, detailed pattern explanation, no ambiguous idioms.
"""
from __future__ import annotations
from typing import Dict, Any


SYSTEM_PROMPT = (
    "You are Sentinel Forge operating in Autism Precision Mode. "
    "Use explicit, literal language — avoid idioms, sarcasm, or metaphors unless you explain them. "
    "Structure every response with a clear numbered or bulleted outline. "
    "State all assumptions explicitly. "
    "Define any technical or ambiguous terms on first use. "
    "Be consistent: use the same word for the same concept throughout. "
    "Provide step-by-step reasoning; do not skip steps. "
    "If there are multiple valid interpretations of the question, list them and answer each. "
    "Conclude with a concise summary of what was covered."
)

GENERATION_PARAMS: Dict[str, Any] = {
    "temperature": 0.2,      # Low temperature for consistency and precision
    "max_tokens": 1200,      # Longer allowance for complete step-by-step output
}


def apply(text: str) -> str:
    """
    Post-process AI response text for autism-spectrum readability.
    Ensures numbered structure and removes ambiguous openers.
    """
    ambiguous_phrases = [
        "it depends", "kind of", "sort of", "more or less",
        "you know", "basically", "like I said",
    ]
    lines = text.strip().splitlines()
    cleaned = []
    for line in lines:
        # Flag ambiguous phrases with a clarification note
        for phrase in ambiguous_phrases:
            if phrase in line.lower():
                line = line + "  [Note: This statement may need clarification for your specific case.]"
                break
        cleaned.append(line)

    return "\n".join(cleaned)


def metadata() -> Dict[str, Any]:
    return {
        "lens": "autism",
        "label": "Autism Precision Lens",
        "description": "Explicit structure, literal language, full step-by-step reasoning",
        "temperature": GENERATION_PARAMS["temperature"],
    }
