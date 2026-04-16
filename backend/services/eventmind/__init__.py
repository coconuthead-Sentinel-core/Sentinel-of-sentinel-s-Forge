"""
Signal Processing Engine — multi-stage signal analysis and response pipeline
integrated into Sentinel Forge as a first-class AI module.

Components:
    core_pulse      — Signal strength analyzer (filters inputs by activation score)
    triangulation   — Multi-perspective input processor (intent, context, signal vectors)
    fulcrum_lens    — Causal and outcome reframing engine
    core_sensor     — Emotional and intent signal detection
    return_vector   — Staged response router based on signal score
    engine          — Master signal processing orchestration engine
"""

from .core_pulse import SignalStrengthAnalyzer
from .triangulation import MultiPerspectiveAnalyzer
from .fulcrum_lens import ContextReframer
from .core_sensor import SignalSensor
from .return_vector import ResponseRouter
from .engine import SignalProcessingEngine

__all__ = [
    "SignalStrengthAnalyzer",
    "MultiPerspectiveAnalyzer",
    "ContextReframer",
    "SignalSensor",
    "ResponseRouter",
    "SignalProcessingEngine",
]
