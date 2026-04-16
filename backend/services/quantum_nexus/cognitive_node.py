"""
Spatial Processing Node — 3D Spatial Processing Architecture
Each node is grounded in one of six Platonic solid geometries,
carrying a base processing frequency, entropy coefficient, and memory zone.

Geometry Primitives:
    TETRAHEDRON    — Transform / Logic-Spark        coords: (1.0, 1.732, 0.816)
    CUBE           — Memory Grounding / Stability   coords: (1.0, 1.0, 1.0)
    OCTAHEDRON     — Processing / Bridge            coords: (1.414, 0.0, 1.414)
    DODECAHEDRON   — Abstraction / High-Order       coords: (1.618, 1.618, 1.618)
    ICOSAHEDRON    — Recursive / High-Complexity    coords: (1.902, 1.176, 0.726)
    ORIGIN         — Core / Reference Point         coords: (0.0, 0.0, 0.0)

Memory Zones (entropy-based):
    ACTIVE_PROCESSING   — entropy > 0.7   (high-entropy)
    PATTERN_EMERGENCE   — entropy 0.3–0.7 (mid-entropy)
    ARCHIVED_STORAGE    — entropy < 0.3   (low-entropy)
"""
from __future__ import annotations

import hashlib
import math
import uuid
import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CognitivePrimitiveType(Enum):
    TETRAHEDRON  = "tetrahedron"
    CUBE         = "cube"
    OCTAHEDRON   = "octahedron"
    DODECAHEDRON = "dodecahedron"
    ICOSAHEDRON  = "icosahedron"
    ORIGIN       = "origin"


class MemoryZoneClassification(Enum):
    ACTIVE_PROCESSING = "active"
    PATTERN_EMERGENCE = "emergence"
    ARCHIVED_STORAGE  = "archived"


# ---------------------------------------------------------------------------
# Geometry constants
# ---------------------------------------------------------------------------

_GEOMETRY_COORDS: Dict[CognitivePrimitiveType, Tuple[float, float, float]] = {
    CognitivePrimitiveType.TETRAHEDRON:  (1.0,   1.732, 0.816),
    CognitivePrimitiveType.CUBE:         (1.0,   1.0,   1.0),
    CognitivePrimitiveType.OCTAHEDRON:   (1.414, 0.0,   1.414),
    CognitivePrimitiveType.DODECAHEDRON: (1.618, 1.618, 1.618),
    CognitivePrimitiveType.ICOSAHEDRON:  (1.902, 1.176, 0.726),
    CognitivePrimitiveType.ORIGIN:       (0.0,   0.0,   0.0),
}

# Base processing frequencies per primitive (Hz) — derived from node geometry
_BASE_FREQUENCIES: Dict[CognitivePrimitiveType, float] = {
    CognitivePrimitiveType.TETRAHEDRON:  7.83,
    CognitivePrimitiveType.CUBE:         6.66,
    CognitivePrimitiveType.OCTAHEDRON:   8.14,
    CognitivePrimitiveType.DODECAHEDRON: 11.11,
    CognitivePrimitiveType.ICOSAHEDRON:  9.63,
    CognitivePrimitiveType.ORIGIN:       13.0,
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SpatialProcessingVector:
    """3D spatial processing descriptor for a cognitive node."""
    primitive_type:      CognitivePrimitiveType
    coordinates:         Tuple[float, float, float]
    elevation_angle:     float = 40.0    # Y-axis cognitive elevation (degrees)
    processing_frequency: float = 1.0
    entropy_signature:   float = 0.5


# ---------------------------------------------------------------------------
# Core class
# ---------------------------------------------------------------------------

class SpatialProcessingNode:
    """
    A spatial processing node with:
    • Platonic solid spatial geometry
    • Geometry-derived processing frequency
    • SHA-256 entropy coefficient
    • Auto-classified memory zone
    """

    DEFAULT_ELEVATION = 40.0   # degrees

    def __init__(
        self,
        node_id: Optional[str] = None,
        content: Any = None,
        primitive_type: CognitivePrimitiveType = CognitivePrimitiveType.CUBE,
    ) -> None:
        self.id               = node_id or f"snode_{uuid.uuid4().hex[:8]}"
        self.content          = content
        self.primitive_type   = primitive_type
        self.cognitive_elevation = self.DEFAULT_ELEVATION

        # Compute in order (spatial_vector needs primitive_type; entropy needs spatial_vector)
        self.entropy_coefficient  = self._calculate_entropy()
        self.spatial_vector       = self._init_spatial_vector()
        self.zone_classification  = self._determine_zone()

        self.processing_threads: list = []
        self.processing_metadata: Dict[str, Any] = {}
        self.creation_timestamp = datetime.datetime.utcnow()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _init_spatial_vector(self) -> SpatialProcessingVector:
        coords = _GEOMETRY_COORDS.get(self.primitive_type, (1.0, 1.0, 1.0))
        return SpatialProcessingVector(
            primitive_type       = self.primitive_type,
            coordinates          = coords,
            elevation_angle      = self.cognitive_elevation,
            processing_frequency = self._calculate_frequency(),
            entropy_signature    = self.entropy_coefficient,
        )

    def _calculate_frequency(self) -> float:
        base = _BASE_FREQUENCIES.get(self.primitive_type, 8.0)
        if self.content:
            content_factor = len(str(self.content)) / 100.0
            return round(base * (1.0 + content_factor * 0.1), 4)
        return base

    def _calculate_entropy(self) -> float:
        if not self.content:
            return 0.5
        content_str  = str(self.content)
        content_hash = hashlib.sha256(content_str.encode()).hexdigest()
        base_entropy = int(content_hash[:8], 16) / 0xFFFFFFFF

        # Spatial entropy modulation (use coords directly)
        coords = _GEOMETRY_COORDS.get(self.primitive_type, (1.0, 1.0, 1.0))
        x, y, z = coords
        spatial_factor   = (x + y + z) / 3.0
        elevation_factor = math.sin(math.radians(self.cognitive_elevation))
        return round(
            (base_entropy * 0.6) + (spatial_factor * 0.2) + (elevation_factor * 0.2),
            4,
        )

    def _determine_zone(self) -> MemoryZoneClassification:
        if self.entropy_coefficient > 0.7:
            return MemoryZoneClassification.ACTIVE_PROCESSING
        elif self.entropy_coefficient > 0.3:
            return MemoryZoneClassification.PATTERN_EMERGENCE
        return MemoryZoneClassification.ARCHIVED_STORAGE

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id":                   self.id,
            "primitive_type":       self.primitive_type.value,
            "coordinates":          self.spatial_vector.coordinates,
            "elevation_angle":      self.cognitive_elevation,
            "processing_frequency": round(self.spatial_vector.processing_frequency, 4),
            "entropy_coefficient":  self.entropy_coefficient,
            "zone_classification":  self.zone_classification.value,
            "created_at":           self.creation_timestamp.isoformat(),
        }
