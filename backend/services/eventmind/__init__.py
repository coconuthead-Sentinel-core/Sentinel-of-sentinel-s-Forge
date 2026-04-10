"""
EventMind — Neurocosmic Construct AI Module
A frequency-based, gravitational cognition engine integrated into Sentinel Forge.

Components:
    core_pulse      — Frequency resonance engine (filters inputs by resonance match)
    triangulation   — Three-vector input processor (intent weight, context vector, frequency match)
    fulcrum_lens    — Backward causality + future outcome reframing
    core_sensor     — Emotional and vibrational intent detection
    return_vector   — Staged response system based on cognitive resonance
"""

from .core_pulse import CorePulse
from .triangulation import TriangulationTelescope
from .fulcrum_lens import FulcrumLens
from .core_sensor import CoreSensor
from .return_vector import ReturnVector
from .engine import EventMindEngine

__all__ = [
    "CorePulse",
    "TriangulationTelescope",
    "FulcrumLens",
    "CoreSensor",
    "ReturnVector",
    "EventMindEngine",
]
