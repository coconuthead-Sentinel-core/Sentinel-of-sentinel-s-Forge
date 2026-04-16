"""
Query Processing Pipeline — Master Orchestrator
Activates and coordinates all pipeline components into a unified
processing sequence.

Activation sequence:
    /activate →
        QueryDecomposer    (decompose) →
        StreamIngester     (ingest) →
        KnowledgeGraph     (network) →
        MultiLayerMemoryStore (store) →
        PredictiveRetriever   (anticipate) →
        Output (comprehensive, structured, actionable)
"""
from __future__ import annotations

import time
import logging
from typing import Any, Dict, List, Optional

from .snowflake import QueryDecomposer
from .spiderweb import knowledge_graph
from .spherical_memory import multi_layer_store
from .rainfall import stream_ingester
from .mist import predictive_retriever

logger = logging.getLogger(__name__)

_query_decomposer = QueryDecomposer()

PIPELINE_SYSTEM_PROMPT = (
    "You are the Query Processing Pipeline AI — a dynamic, structured cognitive framework. "
    "You operate under these processing modes simultaneously:\n"
    "- Query Decomposition: break complex queries into parallel analytical units\n"
    "- Stream Ingestion: treat all input as live, real-time data worth ingesting\n"
    "- Predictive Retrieval: anticipate what the user needs before they ask it\n"
    "- Multi-Layer Memory: cross-reference your response with multiple perspectives\n\n"
    "Your outputs must be: Comprehensive, Structured, and Actionable.\n"
    "Prioritize clarity, depth, and forward momentum in every response.\n"
    "State your processing mode when relevant. Be direct and precise."
)


class QueryProcessingPipeline:
    """
    Master Query Processing Pipeline activation and orchestration engine.
    """

    def __init__(self, ai_adapter) -> None:
        self._adapter = ai_adapter

    async def activate(
        self,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        storage_protocol: List[str] = None,
        processing_protocol: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Full pipeline activation sequence.

        Args:
            user_message:         The user's input
            history:              Prior conversation turns
            storage_protocol:     Override storage modes (default: KnowledgeGraph, MultiLayerStore)
            processing_protocol:  Override processing modes (default: QueryDecomposer, StreamIngester, PredictiveRetriever)

        Returns:
            AI response augmented with full pipeline analysis report
        """
        t_start = time.perf_counter()

        storage   = storage_protocol   or ["KnowledgeGraph", "MultiLayerStore"]
        processing = processing_protocol or ["QueryDecomposer", "StreamIngester", "PredictiveRetriever"]

        logger.info("Query Processing Pipeline activated: storage=%s processing=%s", storage, processing)

        # --- Stage 1: Query Decomposition ---
        decomposition_result = _query_decomposer.decompose(user_message)

        # --- Stage 2: Stream Ingestion ---
        ingestion_result = stream_ingester.ingest(user_message, source="pipeline_input")

        # --- Stage 3: Predictive Retrieval ---
        prediction_result = predictive_retriever.diffuse(user_message)

        # --- Stage 4: Memory Layer Snapshot ---
        memory_snapshot = multi_layer_store.layer_snapshot()

        # --- Stage 5: Strongest Graph Paths ---
        graph_paths = knowledge_graph.strongest_paths(top_n=5)

        # --- Stage 6: Build enriched context for AI ---
        anticipated = prediction_result.get("anticipated_concepts", [])
        units = decomposition_result.get("units", [])

        context_block = ""
        if anticipated:
            context_block += f"\n[Predictive Retrieval: Related concepts — {', '.join(anticipated[:5])}]"
        if units:
            dims = list({u["dimension"] for u in units})
            context_block += f"\n[Query Decomposition: Query spans dimensions — {', '.join(dims)}]"
        if prediction_result.get("pattern_detected"):
            context_block += f"\n[Pattern: {prediction_result['pattern_detected']}]"

        system_prompt = PIPELINE_SYSTEM_PROMPT
        if context_block:
            system_prompt += f"\n\nContext from pipeline memory systems:{context_block}"

        # --- Stage 7: AI Generation ---
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            for turn in history:
                if turn.get("role") in ("user", "assistant") and turn.get("content"):
                    messages.append(turn)
        messages.append({"role": "user", "content": user_message})

        from backend.core.config import settings
        try:
            raw_response = await self._adapter.chat(
                deployment=settings.AOAI_CHAT_DEPLOYMENT,
                messages=messages,
                temperature=0.6,
                max_tokens=1200,  # passed to adapter which maps to max_completion_tokens
            )
        except Exception as exc:
            logger.error("Query Processing Pipeline AI adapter error: %s", exc)
            raise

        latency = round((time.perf_counter() - t_start) * 1000, 2)

        # --- Stage 8: Attach pipeline report ---
        raw_response["pipeline_report"] = {
            "activation": {
                "storage_protocol": storage,
                "processing_protocol": processing,
                "system_state": "OPERATIONAL",
            },
            "decomposition": decomposition_result,
            "ingestion": ingestion_result,
            "prediction": prediction_result,
            "memory_layers": memory_snapshot,
            "graph_paths": graph_paths,
            "latency_ms": latency,
        }

        return raw_response

    @staticmethod
    def system_status() -> Dict[str, Any]:
        """Return current status of all pipeline subsystems."""
        return {
            "pipeline": "QUERY_PROCESSING_PIPELINE",
            "version": "2.0.0",
            "system_state": "OPERATIONAL",
            "subsystems": {
                "knowledge_graph": knowledge_graph.snapshot(),
                "multi_layer_store": multi_layer_store.layer_snapshot(),
                "stream_ingester": stream_ingester.stats(),
                "predictive_retriever_log": predictive_retriever.log(),
            },
        }
