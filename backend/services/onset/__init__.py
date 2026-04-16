"""
Query Processing Pipeline — distributed query decomposition, storage, and response framework
integrated into Sentinel Forge as a first-class AI module.

Components:
    query_decomposer    — Query decomposition into parallel processing sub-units
    knowledge_graph     — Decentralized node network for context storage
    multi_layer_store   — Multi-layer cross-referenced memory store
    stream_ingester     — Real-time data stream ingestion
    predictive_retriever — Anticipatory retrieval engine
    protocol            — Master pipeline activation and orchestration
"""

from .protocol import QueryProcessingPipeline

__all__ = ["QueryProcessingPipeline"]
