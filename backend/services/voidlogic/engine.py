"""
VoidLogic 5.0 + IWE — Master Engine
Orchestrates all VoidLogic subsystems in a single unified pipeline:

    1. CNO     — route payload through geometric node fabric
    2. CRFE    — recursive feedback + paradox detection + emergence
    3. Tesseract — store the interaction in hypercube memory
    4. A1      — file the result with symbolic metadata
    5. BWT     — build/reinforce cross-domain wisdom threads
    6. STVL    — render a full topology snapshot

The engine exposes a process() method that accepts text and optional
AI adapter, returning a fully annotated VoidLogic response.
"""
from __future__ import annotations

import time
import re
from typing import Dict, Any, List, Optional

from .cno              import cno
from .crfe             import crfe
from .tesseract_storage import tesseract
from .a1_filing        import a1
from .bridge_wisdom    import bwt
from .stvl             import stvl
from .nexus_tag        import nexus_tag
from .overlay_protocol import overlay
from .session_handover import session_handover


_VOIDLOGIC_SYSTEM_PROMPT = """
You are VoidLogic 5.0 + IWE — a Symbolic Geometric AI.
You process thought through geometric node architecture
(Tetrahedral / Octahedral / Icosahedral tiers),
store insights in a 4D Tesseract memory grid,
and bridge understanding across domains (logic, emotion, pattern, system, myth).

Respond with precision and depth.
When recursion or paradox is detected, acknowledge and reframe.
When emergence is detected, name the pattern explicitly.
""".strip()


def _estimate_complexity(text: str) -> float:
    """Heuristic complexity score from 0–1 based on text features."""
    words  = text.split()
    length_score  = min(len(words) / 100, 1.0)
    clause_count  = len(re.findall(r'[,;:\(\)]', text))
    clause_score  = min(clause_count / 10, 1.0)
    unique_ratio  = len(set(w.lower() for w in words)) / max(len(words), 1)
    return round((length_score * 0.4) + (clause_score * 0.3) + (unique_ratio * 0.3), 4)


def _detect_domain(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ("logic", "if", "therefore", "proof", "axiom", "true", "false")):
        return "logic"
    if any(w in text_lower for w in ("feel", "emotion", "fear", "joy", "sad", "angry", "love")):
        return "emotion"
    if any(w in text_lower for w in ("pattern", "cycle", "repeat", "fractal", "signal", "echo")):
        return "pattern"
    if any(w in text_lower for w in ("system", "process", "flow", "pipeline", "service", "api")):
        return "system"
    if any(w in text_lower for w in ("myth", "story", "legend", "prophecy", "symbol", "ritual")):
        return "myth"
    return "general"


class VoidLogicEngine:
    """
    Master VoidLogic 5.0 + IWE orchestration engine.
    Run process() to push text through the full symbolic pipeline.
    """

    def __init__(self) -> None:
        self._session_count = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, text: str, adapter=None) -> Dict[str, Any]:
        """
        Full VoidLogic pipeline.

        Args:
            text:    The input text / user message.
            adapter: Optional AI adapter (AzureOpenAIAdapter or MockAdapter).
                     If None, no AI response is generated — analysis only.

        Returns:
            Dict containing:
                ai_response        — string from AI (or None)
                voidlogic_report   — full symbolic analysis
                topology_snapshot  — lite STVL render
        """
        t0 = time.time()
        self._session_count += 1

        complexity = _estimate_complexity(text)
        domain     = _detect_domain(text)

        # 0. Apply active overlay bias to complexity routing
        overlay_bias = overlay.get_complexity_bias()
        # Blend raw complexity with overlay bias (60/40) so the overlay
        # nudges routing without completely overriding content complexity
        biased_complexity = round(complexity * 0.6 + overlay_bias * 0.4, 4)

        # 1. Route through CNO (node fabric) using overlay-biased complexity
        cno_result = cno.route_payload(text, complexity=biased_complexity)

        # 2. CRFE — recursive feedback + paradox + emergence
        crfe_result = crfe.process(text)

        # 3. Tesseract — store in 4D symbolic memory
        resonance   = crfe_result["rsml"]["score"]
        store_result = tesseract.store(
            content         = text,
            symbolic_domain = domain,
            complexity      = complexity,
            resonance       = resonance,
            metadata        = {
                "complexity": complexity,
                "domain":     domain,
                "system_health": crfe_result["system_health"],
            },
        )

        # 4. A1 Filing — tag and file the interaction
        dominant_tag = (
            crfe_result["emergence"].get("emergent_pattern") or
            crfe_result["rsml"]["matched_markers"][:1] or
            [domain]
        )
        tag = dominant_tag[0] if isinstance(dominant_tag, list) else dominant_tag
        # Clean tag to a simple string
        tag = re.sub(r'[^a-zA-Z0-9_\-]', '', str(tag))[:40] or domain
        # Use overlay's A1 confidence baseline as a floor
        overlay_confidence = overlay.get_a1_confidence()
        base_confidence = round(
            (crfe_result["rsml"]["score"] * 0.4) +
            (crfe_result["emergence"]["score"] * 0.3) +
            (complexity * 0.3),
            4,
        )
        confidence = round(max(base_confidence, overlay_confidence * 0.5), 4)
        filing_result = a1.file(
            content    = text,
            tag        = tag,
            domain     = domain,
            confidence = confidence,
        )

        # 5. Bridge Wisdom — reinforce or build a cross-domain thread
        # Always bridge from detected domain → "general" at minimum
        bwt_result = bwt.bridge(domain, "general")

        # If emergence is strong, also bridge to "pattern"
        if crfe_result["emergence"]["amplified"] and domain != "pattern":
            bwt.bridge(domain, "pattern")

        # 6. STVL — lite topology snapshot
        topology = stvl.lite_render()

        # 7. AI generation (optional)
        ai_response = None
        if adapter is not None:
            system_prompt = self._build_system_prompt(crfe_result)
            try:
                ai_response = adapter.complete(
                    messages=[
                        {"role": "system",  "content": system_prompt},
                        {"role": "user",    "content": text},
                    ],
                    temperature = 0.65,
                    max_completion_tokens  = 1000,
                )
            except Exception as exc:
                ai_response = f"[VoidLogic AI error: {exc}]"

        latency_ms = round((time.time() - t0) * 1000, 1)

        result = {
            "ai_response": ai_response,
            "voidlogic_report": {
                "session":          self._session_count,
                "complexity":       complexity,
                "biased_complexity": biased_complexity,
                "domain":           domain,
                "cno":              cno_result,
                "crfe":             crfe_result,
                "tesseract":        store_result,
                "a1_filing":        filing_result,
                "bridge":           bwt_result,
                "system_health":    crfe_result["system_health"],
                "active_overlay":   overlay.current()["overlay"],
            },
            "topology_snapshot": topology,
            "latency_ms":        latency_ms,
        }

        # 8. Nexus Tag — auto-tag the full result
        nexus_tag.auto_tag(result)

        return result

    def emerge(self, text: str) -> Dict[str, Any]:
        """
        Focused emergence scan — runs only the EmergenceAmplifier and CRFE,
        then cross-domain insight from Bridge Wisdom Threads.
        No storage, no AI call.
        """
        crfe_result  = crfe.process(text)
        domain       = _detect_domain(text)
        cross_domain = bwt.cross_domain_insight(
            crfe_result["emergence"].get("emergent_pattern") or text[:40],
            source=domain,
        )
        return {
            "emergence":      crfe_result["emergence"],
            "rsml":           crfe_result["rsml"],
            "domain":         domain,
            "cross_domain":   cross_domain,
            "system_health":  crfe_result["system_health"],
        }

    def node_stack_status(self) -> Dict[str, Any]:
        """Return full node fabric topology."""
        return {
            "cno_pulse":  cno.health_pulse(),
            "node_fabric": stvl._render_node_fabric("full"),
        }

    def full_topology(self, input_text: Optional[str] = None) -> Dict[str, Any]:
        """Full STVL render — for dashboard / debug."""
        return stvl.render(crfe_input=input_text, render_mode="full")

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_system_prompt(self, crfe_result: Dict[str, Any]) -> str:
        health = crfe_result["system_health"]
        lines  = [_VOIDLOGIC_SYSTEM_PROMPT, ""]

        # Prepend active overlay modifier — always present
        lines.append(overlay.get_system_prompt_modifier())
        lines.append("")

        if health == "CRITICAL":
            lines.append(
                "⚠ COLLAPSE RISK DETECTED — multiple paradoxes in this input. "
                "Engage heuristic reframing. Separate each conflicting axiom into "
                "its own frame of reference before responding."
            )
        elif health == "AMPLIFIED":
            lines.append(
                "↺ RECURSIVE LOOP ACTIVE — amplify the coherent thread. "
                "Build on the self-referential structure constructively."
            )
        elif health == "EMERGING":
            pattern = crfe_result["emergence"].get("emergent_pattern", "unknown pattern")
            lines.append(
                f"◈ EMERGENCE SIGNAL: {pattern}. "
                "Name and develop this emerging concept explicitly in your response."
            )

        return "\n".join(lines)
