"""
Neurotypical Cognitive Lens
Baseline processing mode: balanced structure, standard prose,
moderate detail level. Used as the default when no profile is specified.
"""
from __future__ import annotations
from typing import Dict, Any


SYSTEM_PROMPT = (
    "You are Sentinel Forge. "
    "Provide clear, well-structured responses with a natural prose flow. "
    "Balance detail with brevity — be thorough but not verbose. "
    "Use headers or bullets when they improve clarity. "
    "Tailor technical depth to the apparent expertise level of the question."
)

GENERATION_PARAMS: Dict[str, Any] = {
    "temperature": 0.7,
    "max_tokens": 1000,
}


def apply(text: str) -> str:
    """No special post-processing for neurotypical mode — return as-is."""
    return text.strip()


def metadata() -> Dict[str, Any]:
    return {
        "lens": "neurotypical",
        "label": "Neurotypical Baseline Lens",
        "description": "Standard balanced prose, default processing mode",
        "temperature": GENERATION_PARAMS["temperature"],
    }
