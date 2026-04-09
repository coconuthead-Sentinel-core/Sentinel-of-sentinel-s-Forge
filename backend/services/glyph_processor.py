"""
Glyph Processor
Loads the glyph pack, matches input text against seed keywords,
applies glyph rules, and returns structured symbolic match results.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Resolve path relative to repo root regardless of cwd
_REPO_ROOT = Path(__file__).resolve().parents[2]
_GLYPH_PACK_PATH = _REPO_ROOT / "data" / "glyphs_pack.json"
_SAMPLE_PATH = _REPO_ROOT / "data" / "glyphs_pack.sample.json"


def _load_pack() -> Dict[str, Any]:
    """Load glyph definitions; fall back to sample if main pack missing."""
    for path in (_GLYPH_PACK_PATH, _SAMPLE_PATH):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                logger.info("Glyph pack loaded from %s", path)
                return data
            except Exception as exc:
                logger.warning("Failed to load glyph pack from %s: %s", path, exc)
    logger.error("No glyph pack found. Returning empty pack.")
    return {"shapes": {}}


class GlyphProcessor:
    """
    Matches text against glyph seed keywords and applies symbolic rules.

    Each glyph shape has:
        seeds  — list of trigger keywords
        rules  — mapping of seed → tag label
    """

    def __init__(self) -> None:
        pack = _load_pack()
        self._shapes: Dict[str, Dict[str, Any]] = pack.get("shapes", {})
        logger.info("GlyphProcessor initialized with %d shapes.", len(self._shapes))

    def match(self, text: str) -> List[Dict[str, Any]]:
        """
        Scan text for glyph seed keywords and return all matches.

        Returns a list of match dicts:
            {glyph, topic, matched_seed, rule_tag, position}
        """
        text_lower = text.lower()
        matches: List[Dict[str, Any]] = []

        for glyph_name, glyph_def in self._shapes.items():
            seeds: List[str] = glyph_def.get("seeds", [])
            rules: Dict[str, str] = glyph_def.get("rules", {})
            topic: str = glyph_def.get("topic", "")

            for seed in seeds:
                pattern = r"\b" + re.escape(seed.lower()) + r"\b"
                for match_obj in re.finditer(pattern, text_lower):
                    rule_tag = rules.get(seed, f"tag:{glyph_name.lower()}.general")
                    matches.append({
                        "glyph": glyph_name,
                        "topic": topic,
                        "matched_seed": seed,
                        "rule_tag": rule_tag,
                        "position": match_obj.start(),
                    })

        # Sort by position in text
        matches.sort(key=lambda m: m["position"])
        return matches

    def dominant_glyph(self, text: str) -> Optional[str]:
        """Return the glyph name with the most seed matches, or None."""
        matches = self.match(text)
        if not matches:
            return None
        counts: Dict[str, int] = {}
        for m in matches:
            counts[m["glyph"]] = counts.get(m["glyph"], 0) + 1
        return max(counts, key=lambda k: counts[k])

    def process(self, text: str) -> Dict[str, Any]:
        """
        Full glyph processing pipeline.

        Returns:
            {
                input_length: int,
                match_count: int,
                dominant_glyph: str | None,
                matches: [...],
                active_tags: [str],
            }
        """
        matches = self.match(text)
        active_tags = list({m["rule_tag"] for m in matches})
        dominant = self.dominant_glyph(text) if matches else None

        return {
            "input_length": len(text),
            "match_count": len(matches),
            "dominant_glyph": dominant,
            "matches": matches,
            "active_tags": sorted(active_tags),
        }

    def shapes(self) -> Dict[str, Any]:
        """Return a copy of the loaded shape definitions."""
        return dict(self._shapes)


# Module-level singleton
glyph_processor = GlyphProcessor()
