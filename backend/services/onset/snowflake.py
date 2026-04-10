"""
Snowflake Processor
Decomposes a complex query into discrete processing flakes —
each flake is an independently analyzable sub-query or data dimension.

Like a snowflake's fractal structure, each flake is unique
but part of a coherent whole.
"""
from __future__ import annotations

import re
from typing import List, Dict, Any


# Dimension classifiers — what category does each flake belong to?
_DIMENSION_PATTERNS = {
    "temporal":    r'\b(when|time|date|year|month|day|now|before|after|recent|current|future|past)\b',
    "causal":      r'\b(why|because|cause|reason|result|effect|impact|due to|leads to)\b',
    "comparative": r'\b(compare|versus|vs|difference|better|worse|more|less|best|worst)\b',
    "procedural":  r'\b(how|step|process|procedure|method|way|approach|implement|build|create)\b',
    "definitional":r'\b(what|define|meaning|explain|describe|is a|are|refers to)\b',
    "evaluative":  r'\b(evaluate|assess|review|judge|rate|score|quality|performance|good|bad)\b',
    "relational":  r'\b(connect|relate|link|between|relationship|associate|depends|integrates)\b',
}


class SnowflakeProcessor:
    """
    Fractal Query Decomposition Engine.
    Breaks a complex query into parallel processing flakes.
    """

    def decompose(self, query: str) -> Dict[str, Any]:
        """
        Decompose a query into snowflake flakes.

        Returns:
            {
                flakes: [{id, text, dimension, weight}],
                flake_count: int,
                primary_dimension: str,
                complexity_score: float
            }
        """
        # Split on natural boundaries: sentences, semicolons, bullet points
        raw_flakes = re.split(r'[.!?;]|\band\b|\balso\b|\bplus\b|\badditionally\b', query)
        raw_flakes = [f.strip() for f in raw_flakes if len(f.strip()) > 3]

        if not raw_flakes:
            raw_flakes = [query]

        flakes = []
        dimension_counts: Dict[str, int] = {}

        for i, flake_text in enumerate(raw_flakes):
            dimension = self._classify_dimension(flake_text)
            weight = round(len(flake_text.split()) / max(len(query.split()), 1), 4)
            dimension_counts[dimension] = dimension_counts.get(dimension, 0) + 1

            flakes.append({
                "id": f"flake_{i+1}",
                "text": flake_text,
                "dimension": dimension,
                "weight": weight,
            })

        primary = max(dimension_counts, key=lambda k: dimension_counts[k]) if dimension_counts else "general"
        complexity = round(min(len(flakes) / 5, 1.0), 4)

        return {
            "flakes": flakes,
            "flake_count": len(flakes),
            "primary_dimension": primary,
            "complexity_score": complexity,
            "dimension_distribution": dimension_counts,
        }

    def _classify_dimension(self, text: str) -> str:
        text_lower = text.lower()
        for dimension, pattern in _DIMENSION_PATTERNS.items():
            if re.search(pattern, text_lower):
                return dimension
        return "general"
