"""
Knowledge Graph
Decentralized context storage that maps relationships between concepts.
Nodes are weighted by access frequency.
Edges strengthen with repeated co-occurrence — frequently accessed connections
become primary retrieval paths.
"""
from __future__ import annotations

import time
from typing import Dict, Any, List, Optional


class KnowledgeNode:
    def __init__(self, concept: str) -> None:
        self.concept = concept
        self.weight: float = 1.0
        self.connections: Dict[str, float] = {}  # concept → link strength
        self.last_accessed: float = time.time()
        self.access_count: int = 1

    def access(self) -> None:
        self.weight = round(min(self.weight + 0.1, 5.0), 4)
        self.last_accessed = time.time()
        self.access_count += 1

    def connect(self, other_concept: str, strength: float = 1.0) -> None:
        existing = self.connections.get(other_concept, 0.0)
        self.connections[other_concept] = round(min(existing + strength, 10.0), 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept": self.concept,
            "weight": self.weight,
            "connections": self.connections,
            "access_count": self.access_count,
        }


class KnowledgeGraph:
    """
    Dynamic knowledge graph for concept relationship mapping.
    Stores concepts as nodes; relationships as weighted edges.
    """

    def __init__(self, max_nodes: int = 500) -> None:
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._max_nodes = max_nodes

    def ingest(self, concepts: List[str]) -> Dict[str, Any]:
        """
        Add concepts to the graph and strengthen edges between co-occurring concepts.

        Returns graph stats after ingestion.
        """
        if len(self._nodes) >= self._max_nodes:
            self._prune()

        for concept in concepts:
            if concept in self._nodes:
                self._nodes[concept].access()
            else:
                self._nodes[concept] = KnowledgeNode(concept)

        for i, c1 in enumerate(concepts):
            for c2 in concepts[i+1:]:
                if c1 != c2:
                    self._nodes[c1].connect(c2, 0.5)
                    self._nodes[c2].connect(c1, 0.5)

        return self.snapshot()

    def retrieve(self, concept: str, depth: int = 2) -> Dict[str, Any]:
        """
        Retrieve a concept node and its connected neighbours up to `depth` hops.
        """
        if concept not in self._nodes:
            return {"found": False, "concept": concept}

        node = self._nodes[concept]
        node.access()

        result = {
            "found": True,
            "node": node.to_dict(),
            "neighbours": {},
        }

        if depth > 1:
            for connected_concept in list(node.connections.keys())[:10]:
                if connected_concept in self._nodes:
                    result["neighbours"][connected_concept] = self._nodes[connected_concept].to_dict()

        return result

    def strongest_paths(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Return the top N strongest edges across the graph."""
        edges = []
        seen = set()
        for concept, node in self._nodes.items():
            for connected, strength in node.connections.items():
                key = tuple(sorted([concept, connected]))
                if key not in seen:
                    seen.add(key)
                    edges.append({"from": concept, "to": connected, "strength": strength})
        return sorted(edges, key=lambda e: e["strength"], reverse=True)[:top_n]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "node_count": len(self._nodes),
            "top_nodes": sorted(
                [n.to_dict() for n in self._nodes.values()],
                key=lambda n: n["weight"], reverse=True
            )[:10],
        }

    def _prune(self) -> None:
        """Remove the lowest-weight 20% of nodes."""
        sorted_nodes = sorted(self._nodes.items(), key=lambda x: x[1].weight)
        prune_count = len(self._nodes) // 5
        for concept, _ in sorted_nodes[:prune_count]:
            del self._nodes[concept]


# Module-level singleton
knowledge_graph = KnowledgeGraph()
