from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
import uuid

class Entity(BaseModel):
    """Base class for all domain entities."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Strict mode: ignore extra fields passed during initialization
    model_config = ConfigDict(extra="ignore")

class Note(Entity):
    """
    A discrete unit of information stored in the Memory Lattice.
    Pure domain model: No database aliases here.
    """
    text: str
    tag: str
    vector: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemorySnapshot(Entity):
    """A snapshot of the system's cognitive state."""
    summary: str
    active_nodes: int
    entropy_level: float
