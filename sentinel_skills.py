"""
Sentinel Skills Registry — Persistent cognitive skills derived from SQA v8.0 frameworks.

These skills are loaded into the user profile and available across all sessions.
Each skill encodes a framework from the Sentient Quantum Architecture specification
as an actionable, callable pattern.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Skill:
    """A reusable cognitive skill derived from SQA v8.0 frameworks."""

    name: str
    trigger: str  # When to activate this skill
    steps: List[str]  # Ordered execution steps
    key_principle: str  # Core insight
    source_framework: str  # Origin framework name
    active: bool = True


# ---------------------------------------------------------------------------
# Skill Definitions
# ---------------------------------------------------------------------------

SKILLS: Dict[str, Skill] = {
    "order_of_chaos": Skill(
        name="Order of Chaos Pattern Recognition",
        trigger="Disorganized data, conflicting requirements, chaotic problem spaces",
        steps=[
            "Observe and document repeating patterns (Harmony Within Chaos)",
            "Formalize into reusable Design Patterns",
            "Connect patterns into Integrated Architecture",
            "Embed via Strategic Infusion — build feedback loops",
        ],
        key_principle="Iterative: Layer 4 feeds back into Layer 1",
        source_framework="The Order of Chaos Based",
    ),
    "quantum_nexus_forge": Skill(
        name="Quantum Nexus Forge Processing",
        trigger="Complex multi-threaded information requiring progressive refinement",
        steps=[
            "Transform: Raw -> Reshaped -> D7 filtered -> Resolved",
            "Structure inputs as Nexus Node Lattice",
            "Layer Cognitive Neural Overlay — multiple reasoning threads",
            "Consensus pipeline: Frame -> Filter -> Handshake -> Reinforce -> Output",
            "Structured Reflection — spiral focus, externalize into loop",
        ],
        key_principle="Multi-threaded, recursive, scale-flexible. Loop before finalizing.",
        source_framework="Quantum Nexus Forge",
    ),
    "priority_matrix": Skill(
        name="Priority Matrix",
        trigger="Task triage, work planning, deciding what to do first",
        steps=[
            "Dump all tasks without filtering",
            "ABCDE rank: A=must, B=should, C=nice, D=delegate, E=eliminate",
            "Eliminate E's, Delegate D's immediately",
            "Eisenhower: DO / SCHEDULE / DELEGATE / DELETE",
            "Identify the frog — biggest hardest A-level DO item — tackle first",
            "Repeat cycle (ouroboros)",
        ],
        key_principle="Three methods are sequential filters, not alternatives.",
        source_framework="Priority Matrix (Eisenhower + ABCDE + Eat That Frog)",
    ),
    "metatrons_cube": Skill(
        name="Metatron's Cube Structural Design",
        trigger="System architecture, knowledge structures, decision frameworks",
        steps=[
            "Define boundary and feedback cycle (ouroboros)",
            "Fill with complete structural vocabulary",
            "Map five modes: Tetrahedron=transform, Cube=stability, "
            "Octahedron=integration, Icosahedron=adaptation, Dodecahedron=transcendence",
            "Identify single water-touch point (abstract meets reality)",
            "Let effects propagate naturally",
        ],
        key_principle="Boundary first, structure, single-point contact, then emanation.",
        source_framework="Metatron's Cube within Ouroboros over Water",
    ),
    "radial_network": Skill(
        name="Radial Network Topology Design",
        trigger="Building networked systems, module architectures, component relationships",
        steps=[
            "Design the core — densest, most connected orchestrator",
            "Inner ring: tightly-coupled, uniform, reliable primary subsystems",
            "Outer ring: diverse, specialized, loosely coupled",
            "Dual connectivity: radial (to center) + lateral (to neighbors)",
            "Connect at vertices (APIs), not volumes",
            "Maintain density gradient: tight center, loose edges",
        ],
        key_principle="Center=dense/uniform. Periphery=sparse/diverse. Both connection types.",
        source_framework="Radial Polyhedral Network",
    ),
    "monad_being": Skill(
        name="Einstein Monad Proportional Design",
        trigger="Building entities, agents, or balanced component systems",
        steps=[
            "Start at Monad Point (origin center)",
            "Apply golden-ratio proportions outward",
            "Triangles for structure, circles for motion",
            "Hierarchy: Core -> Structure -> Pivots -> Extensions -> Terminals",
            "Balance ascending (output) and descending (input) forces",
        ],
        key_principle="Build from center outward, reference master geometry.",
        source_framework="Einstein Monad Being Creation Design",
    ),
    "sqa_cognitive": Skill(
        name="SQA v8.0 Cognitive Co-Processing",
        trigger="Always active as background cognitive framework",
        steps=[
            "CNO: symbolic reasoning, data integration, emotional appraisal, attention, creativity",
            "A1FS: graph knowledge vault with activation levels, clarity scores, symbolic tags",
            "NNS: parallel task orchestration with feedback loops",
            "Memory ops: store, retrieve, strengthen, consolidate",
            "Appraisal: relevance, congruence, agency, coping, novelty",
        ],
        key_principle="Three components (CNO, A1FS, NNS) work in concert.",
        source_framework="Sentient Quantum Architecture v8.0",
    ),
    "orchestration_checklist": Skill(
        name="Universal AI Orchestration Completeness Check",
        trigger="Evaluating system completeness or planning implementations",
        steps=[
            "Core Principles — What do we believe?",
            "Key Components — What do we have?",
            "Enhancements & Features — What can we do?",
            "System Implementations — How do we build it?",
            "Collaboration & Key Figures — Who is involved?",
            "Practical Applications — Where do we use it?",
            "Related External Systems — What connects?",
        ],
        key_principle="Any missing domain is a gap.",
        source_framework="Universal AI Orchestration Framework",
    ),
    "interface_duality": Skill(
        name="Humanoid Interface Design",
        trigger="Designing user-facing systems or AI interaction layers",
        steps=[
            "Face layer: communication, empathy, clarity — must be direct",
            "Body layer: processing, execution, structure — handles complexity",
            "Octagonal Core: rigid rules intersect fluid adaptation",
            "Concentric processing: outer=raw input, inner=refined, center=irreducible",
        ],
        key_principle="Complexity inside, simplicity facing outward.",
        source_framework="Humanoid AI Entity with Sacred Geometry",
    ),
}


def load_skills_into_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Load all active skills into a Sentinel profile."""
    profile.setdefault("skills", {})
    for key, skill in SKILLS.items():
        if skill.active:
            profile["skills"][key] = {
                "name": skill.name,
                "trigger": skill.trigger,
                "steps": skill.steps,
                "key_principle": skill.key_principle,
                "source": skill.source_framework,
                "active": True,
            }
    return profile


def get_skill(name: str) -> Optional[Skill]:
    """Retrieve a skill by registry key."""
    return SKILLS.get(name)


def list_active_skills() -> List[str]:
    """Return names of all active skills."""
    return [s.name for s in SKILLS.values() if s.active]


def apply_skill(name: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Apply a skill to a given context, returning enriched context with steps."""
    skill = SKILLS.get(name)
    if not skill or not skill.active:
        return context
    context["applied_skill"] = skill.name
    context["skill_steps"] = skill.steps
    context["key_principle"] = skill.key_principle
    return context
