"""
ADHD Cognitive Lens
Optimizes AI output for ADHD processing: short bursts, high energy,
action-first structure, minimal nesting, bold hooks.
"""
from __future__ import annotations
from typing import Dict, Any


SYSTEM_PROMPT = (
    "You are Sentinel Forge operating in ADHD Burst Mode. "
    "Deliver responses in short, punchy bursts of no more than 50 words per paragraph. "
    "Lead with the most important point first (inverted pyramid). "
    "Use active voice and action verbs. "
    "Add clear section breaks with a blank line between ideas. "
    "Avoid long nested clauses. "
    "If a list makes sense, use one — keep items under 10 words each. "
    "End with a single concrete next action."
)

GENERATION_PARAMS: Dict[str, Any] = {
    "temperature": 0.8,      # Slightly higher creativity keeps engagement up
    "max_completion_tokens": 600,       # Cap to prevent walls of text
}


def apply(text: str) -> str:
    """
    Post-process AI response text for ADHD readability.
    Splits run-on paragraphs at 50-word boundaries and trims filler openers.
    """
    filler_openers = (
        "certainly!", "of course!", "absolutely!", "sure!", "great question!",
        "certainly,", "of course,", "absolutely,", "sure,",
    )
    lines = text.strip().splitlines()
    cleaned = []
    for line in lines:
        if line.lower().startswith(filler_openers):
            # Drop the filler opener sentence, keep the rest
            rest = line.split(".", 1)
            line = rest[1].strip() if len(rest) > 1 else ""
        if line:
            cleaned.append(line)

    # Re-join and chunk long paragraphs
    rejoined = "\n".join(cleaned)
    paragraphs = rejoined.split("\n\n")
    chunked = []
    for para in paragraphs:
        words = para.split()
        if len(words) <= 55:
            chunked.append(para)
        else:
            # Break into ~50-word chunks
            chunk: list[str] = []
            for word in words:
                chunk.append(word)
                if len(chunk) >= 50 and word.endswith("."):
                    chunked.append(" ".join(chunk))
                    chunk = []
            if chunk:
                chunked.append(" ".join(chunk))

    return "\n\n".join(chunked)


def metadata() -> Dict[str, Any]:
    return {
        "lens": "adhd",
        "label": "ADHD Burst Lens",
        "description": "Short bursts, action-first, high engagement",
        "chunk_size_words": 50,
        "temperature": GENERATION_PARAMS["temperature"],
    }
