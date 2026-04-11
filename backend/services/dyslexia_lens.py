"""
Dyslexia Cognitive Lens
Optimizes AI output for dyslexia-friendly reading: short sentences,
plain words, spatial anchors, visual rhythm, no dense blocks of text.
"""
from __future__ import annotations
from typing import Dict, Any


SYSTEM_PROMPT = (
    "You are Sentinel Forge operating in Dyslexia Spatial Mode. "
    "Use short sentences — aim for under 15 words per sentence. "
    "Choose plain, common words over complex alternatives (e.g., 'use' not 'utilize'). "
    "Break content into small visual chunks with frequent line breaks. "
    "Use bullet points or numbered steps instead of long paragraphs. "
    "Avoid justified text patterns — left-align your logic. "
    "Repeat key terms consistently rather than using synonyms that may confuse. "
    "Highlight the most important word or phrase in each section by placing it on its own line. "
    "Keep the total response scannable — the reader should be able to find the answer in 10 seconds."
)

GENERATION_PARAMS: Dict[str, Any] = {
    "temperature": 0.5,
    "max_completion_tokens": 700,
}

_COMPLEX_TO_PLAIN = {
    "utilize": "use",
    "demonstrate": "show",
    "implement": "build",
    "facilitate": "help",
    "consequently": "so",
    "nevertheless": "but",
    "approximately": "about",
    "subsequently": "then",
    "commence": "start",
    "terminate": "end",
    "endeavour": "try",
    "pertaining to": "about",
    "in the event that": "if",
    "with regard to": "about",
}


def apply(text: str) -> str:
    """
    Post-process AI response text for dyslexia-friendly reading.
    Replaces complex words with plain equivalents and enforces short line rhythm.
    """
    for complex_word, plain_word in _COMPLEX_TO_PLAIN.items():
        text = text.replace(complex_word, plain_word)
        text = text.replace(complex_word.capitalize(), plain_word.capitalize())

    # Break any sentence longer than 20 words at a comma or conjunction
    sentences = text.split(". ")
    processed = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 20:
            # Try to split at first conjunction after word 10
            conjunctions = [" and ", " but ", " or ", " so ", " yet "]
            split_done = False
            for conj in conjunctions:
                idx = sentence.lower().find(conj, len(" ".join(words[:8])))
                if idx != -1:
                    part1 = sentence[:idx].strip()
                    part2 = sentence[idx + len(conj):].strip()
                    processed.append(part1 + ".")
                    processed.append(part2.capitalize())
                    split_done = True
                    break
            if not split_done:
                processed.append(sentence)
        else:
            processed.append(sentence)

    return " ".join(processed)


def metadata() -> Dict[str, Any]:
    return {
        "lens": "dyslexia",
        "label": "Dyslexia Spatial Lens",
        "description": "Short sentences, plain words, visual rhythm, scannable layout",
        "max_sentence_words": 15,
        "temperature": GENERATION_PARAMS["temperature"],
    }
