"""
Dyscalculia Cognitive Lens
Optimizes AI output for dyscalculia processing:
  • Replaces bare numbers with conceptual magnitude descriptions
  • Adds visual grouping hints (●●● style) next to numeric quantities
  • Rewrites ratio/percentage language into plain comparative language
  • Avoids implicit math — always explains "what this number means"
"""
from __future__ import annotations

import re
from typing import Dict, Any


SYSTEM_PROMPT = (
    "You are Sentinel Forge operating in Dyscalculia Alternative Logic Mode. "
    "When you use any number, always immediately describe what it means conceptually "
    "— do not leave numbers to speak for themselves. "
    "Prefer comparisons ('about as many as...', 'roughly twice the size of...') "
    "over raw figures whenever possible. "
    "If you must list a number, follow it with a brief visual scale like: "
    "'5 (●●●●●)' or '12 (about a dozen, ◐◐●●)'. "
    "Avoid fractions; use 'roughly half', 'about a quarter' instead. "
    "Never assume the reader can mentally manipulate numbers — spell out every quantity's meaning. "
    "Structure responses with clear visual spacing so each idea stands alone."
)

GENERATION_PARAMS: Dict[str, Any] = {
    "temperature": 0.6,
    "max_completion_tokens":  900,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _visual_group(n: int) -> str:
    """Generate a visual dot-group representation for small numbers."""
    if n <= 0:
        return ""
    if n <= 10:
        return "●" * n
    groups    = n // 5
    remainder = n % 5
    return "◐" * groups + "●" * remainder


def _magnitude_label(n: int) -> str:
    if n == 0:       return "zero"
    if n == 1:       return "one"
    if n < 5:        return "a few"
    if n < 10:       return "several"
    if n < 20:       return "a dozen or so"
    if n < 50:       return "a couple dozen"
    if n < 100:      return "nearly a hundred"
    if n < 1_000:    return "hundreds"
    if n < 10_000:   return "thousands"
    return "a very large number"


_PERCENT_RE = re.compile(r'(\d+(?:\.\d+)?)\s*%')
_NUMBER_RE  = re.compile(r'\b(\d+)\b')


def _annotate_numbers(text: str) -> str:
    """Append visual/conceptual hints to bare numbers and percentages."""

    def replace_percent(m: re.Match) -> str:
        val = float(m.group(1))
        if val <= 0:    label = "none"
        elif val < 10:  label = "a small fraction"
        elif val < 25:  label = "about a quarter or less"
        elif val < 50:  label = "less than half"
        elif val == 50: label = "exactly half"
        elif val < 75:  label = "more than half"
        elif val < 100: label = "most"
        else:           label = "all"
        return f"{m.group(0)} ({label})"

    def replace_number(m: re.Match) -> str:
        n = int(m.group(1))
        if n > 999:
            return m.group(0)       # skip large numbers (already complex)
        dots = _visual_group(n)
        label = _magnitude_label(n)
        if dots:
            return f"{m.group(0)} [{dots} — {label}]"
        return f"{m.group(0)} [{label}]"

    # Apply percent first, then plain numbers
    text = _PERCENT_RE.sub(replace_percent, text)
    text = _NUMBER_RE.sub(replace_number,  text)
    return text


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def apply(text: str) -> str:
    """
    Post-process AI response for dyscalculia accessibility.
    Annotates numbers with visual groupings and conceptual magnitude labels.
    """
    return _annotate_numbers(text.strip())


def metadata() -> Dict[str, Any]:
    return {
        "lens":        "dyscalculia",
        "label":       "Dyscalculia Alternative Logic Lens",
        "description": "Visual groupings, magnitude descriptions, no implicit math",
        "temperature": GENERATION_PARAMS["temperature"],
    }
