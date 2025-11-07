from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    data: Any
    pool_id: Optional[str] = Field(default=None, description="Target pool ID")


class ProcessResponse(BaseModel):
    input_id: str
    output_id: str
    result: Any
    processing_time: float
    pool_used: str


class StatusResponse(BaseModel):
    system_id: str
    total_pools: int
    total_processors: int
    total_executions: int
    pool_status: Dict[str, Dict[str, Any]]
    global_bridges: int
    log_entries: int
    platform: str


class StressRequest(BaseModel):
    iterations: int = Field(ge=0, default=100)
    concurrent: bool = False
    async_mode: bool = Field(
        default=False, description="Run as background job and return job_id"
    )


class StressResult(BaseModel):
    iterations: int
    successes: int
    failures: int
    success_rate: float
    total_time: float
    throughput: float
    system_status: Dict[str, Any]


class JobSubmitResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[StressResult] = None
    error: Optional[str] = None


class PoolCreateRequest(BaseModel):
    pool_id: str
    initial_size: int = Field(ge=1, le=100, default=3)


class RebuildRequest(BaseModel):
    default_pools: int = Field(ge=0, le=50, default=2)
    pool_size: int = Field(ge=1, le=100, default=5)


# --- Cognition management ---


class SymbolicRules(BaseModel):
    rules: Dict[str, str]


class SetRulesRequest(BaseModel):
    rules: Dict[str, str]


class MemorySnapshot(BaseModel):
    size: int
    capacity: int
    top_preview: list[str] = Field(default_factory=list)


class PrimeMetrics(BaseModel):
    window: int
    entropy: float
    unique_tokens: int
    token_count: int
    top_tokens: list[tuple[str, int]]


class Suggestions(BaseModel):
    suggestions: list[dict]


# --- Sync / Glyphic protocol ---


class SyncUpdateRequest(BaseModel):
    agent: str
    state: Dict[str, Any] = Field(default_factory=dict)


class AgentSnapshot(BaseModel):
    agent: str
    timestamp: float
    payload: Dict[str, Any]
    glyphic_signature: tuple[int, int, int, int, int]


class SyncSnapshot(BaseModel):
    session_id: str
    agents: list[str]
    sequence: list[str]
    sequence_validation: Dict[str, Any]
    states: Dict[str, AgentSnapshot]
    events: list[Dict[str, Any]]


class GlyphValidateRequest(BaseModel):
    sequence: list[str]


class GlyphValidateResponse(BaseModel):
    valid: bool
    reason: str


class BootStep(BaseModel):
    glyph: str
    name: str
    index: int
