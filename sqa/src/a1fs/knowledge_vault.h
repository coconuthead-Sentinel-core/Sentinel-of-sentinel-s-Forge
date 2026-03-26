#pragma once
#include "memory_node.h"
#include <functional>
#include <mutex>
#include <optional>
#include <vector>

namespace sqa::a1fs {

/// Graph-based knowledge vault with associative retrieval.
/// Thread-safe for concurrent read/write access.
class KnowledgeVault {
public:
    explicit KnowledgeVault(size_t capacity = 1024);

    /// Store a new memory node and return its ID.
    Id store(MemoryNode node);

    /// Retrieve a node by ID.
    std::optional<MemoryNode> get(const Id& id) const;

    /// Find nodes similar to query text using Jaccard similarity on tokens.
    std::vector<std::pair<Id, double>> retrieve_similar(
        const std::string& query, int top_k = 5) const;

    /// Strengthen a memory trace (bump activation).
    void strengthen(const Id& id, double amount = 0.1);

    /// Add a relationship edge between two nodes.
    void link(const Id& source, const Id& target,
              RelationType type, double weight = 1.0);

    /// Get edges for a given node.
    std::vector<RelationshipEdge> edges_for(const Id& id) const;

    /// Return total node count.
    size_t size() const;

    /// Return full snapshot as JSON.
    json snapshot() const;

    /// Clear all nodes and edges.
    void clear();

private:
    size_t capacity_;
    mutable std::mutex mutex_;
    std::unordered_map<Id, MemoryNode> nodes_;
    std::vector<RelationshipEdge> edges_;

    /// Jaccard similarity between two strings (token sets).
    static double jaccard(const std::string& a, const std::string& b);
};

}  // namespace sqa::a1fs
