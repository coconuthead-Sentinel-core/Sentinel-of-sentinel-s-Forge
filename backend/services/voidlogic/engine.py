"""
SymbolicReasoningEngine — Master Orchestrator
Coordinates all subsystems into a single unified processing pipeline:

    1. ComputeNodeRouter      — route payload through the geometric node fabric
    2. RecursiveFeedbackEngine — recursive pattern detection, paradox resolution, emergence
    3. ContextMemoryStore     — store the interaction in multi-dimensional session memory
    4. SymbolicMemoryIndex    — file the result with metadata and drift monitoring
    5. KnowledgeBridgeThreads — build/reinforce cross-domain knowledge threads
    6. TopologyRenderer       — render a full topology snapshot

Exposes a process() method that accepts text and an optional AI adapter,
returning a fully annotated symbolic reasoning response.
"""
from __future__ import annotations

import time
import re
from typing import Dict, Any, List, Optional

from .cno               import cno
from .crfe              import crfe
from .tesseract_storage import context_memory
from .a1_filing         import a1
from .bridge_wisdom     import knowledge_bridge
from .stvl              import stvl
from .nexus_tag         import nexus_tag
from .overlay_protocol  import overlay
from .session_handover  import session_handover


_SYMBOLIC_REASONING_SYSTEM_PROMPT = """
You are a Symbolic Reasoning AI assistant.
You analyze input through a structured pipeline:
- Recursive pattern detection (loops, self-references, structural recursion)
- Paradox identification and contextual reframing
- Emergence detection (weak signals that resolve into larger patterns)
- Cross-domain knowledge bridging (logic, emotion, pattern, system)

Respond with precision and depth.
When recursion or paradox is detected, acknowledge and reframe it clearly.
When an emergent pattern is detected, name it explicitly.
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
    if any(w in text_lower for w in ("narrative", "story", "legend", "symbol", "framework", "concept")):
        return "narrative"
    return "general"


class SymbolicReasoningEngine:
    """
    Master symbolic reasoning orchestration engine.
    Run process() to push text through the full analysis pipeline.
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
                reasoning_report   — full symbolic analysis
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

        # 3. Context Memory — store the interaction
        resonance   = crfe_result["rsml"]["score"]
        store_result = context_memory.store(
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

        # 4. Symbolic Memory Index — tag and file the interaction
        dominant_tag = (
            crfe_result["emergence"].get("emergent_pattern") or
            crfe_result["rsml"]["matched_markers"][:1] or
            [domain]
        )
        tag = dominant_tag[0] if isinstance(dominant_tag, list) else dominant_tag
        # Clean tag to a simple string
        tag = re.sub(r'[^a-zA-Z0-9_\-]', '', str(tag))[:40] or domain
        # Use overlay's A1 confidence baseline as a floor
        overlay_confidence = overlay.get_memory_confidence()
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
        bwt_result = knowledge_bridge.bridge(domain, "general")

        # If emergence is strong, also bridge to "pattern"
        if crfe_result["emergence"]["amplified"] and domain != "pattern":
            knowledge_bridge.bridge(domain, "pattern")

        # 6. STVL — lite topology snapshot
        topology = stvl.lite_render()

        # 7. AI generation (optional)
        ai_response = None
        if adapter is not None:
            system_prompt = self._build_system_prompt(crfe_result)
            try:
                ai_response = adapter.complete(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": text},
                    ],
                    temperature = 0.65,
                    max_completion_tokens  = 1000,
                )
            except Exception as exc:
                ai_response = f"[VoidLogic AI error: {exc}]"

        latency_ms = round((time.time() - t0) * 1000, 1)

        result = {
            "ai_response": ai_response,
            "reasoning_report": {
                "session":          self._session_count,
                "complexity":       complexity,
                "biased_complexity": biased_complexity,
                "domain":           domain,
                "cno":              cno_result,
                "crfe":             crfe_result,
                "context_memory":   store_result,
                "symbolic_memory":  filing_result,
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
        cross_domain = knowledge_bridge.cross_domain_insight(
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
        lines  = [_SYMBOLIC_REASONING_SYSTEM_PROMPT, ""]

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
