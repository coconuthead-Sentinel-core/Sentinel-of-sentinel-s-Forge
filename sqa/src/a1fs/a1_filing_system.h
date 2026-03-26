#pragma once
/**
 * A1FilingSystem — Top-level facade for the graph-based memory system.
 */
#include "knowledge_vault.h"
#include "consolidation_engine.h"

namespace sqa::a1fs {

class A1FilingSystem {
public:
    explicit A1FilingSystem(size_t capacity = 1024);

    void configure(const json& cfg);

    /// Store an episodic memory from text and tags.
    Id store_episodic(const std::string& text,
                      const std::vector<std::string>& tags,
                      const json& metadata = json::object());

    /// Retrieve similar memories.
    std::vector<std::pair<Id, double>> retrieve_similar(
        const std::string& query, int top_k = 5) const;

    /// Strengthen a memory trace.
    void strengthen(const Id& id, double amount = 0.1);

    /// Link two memories.
    void link(const Id& source, const Id& target,
              RelationType type = RelationType::Associative,
              double weight = 1.0);

    /// Run memory consolidation.
    int consolidate();

    /// Get snapshot.
    json snapshot() const;

    /// Clear all memory.
    void clear();

    /// Node count.
    size_t size() const;

    /// Access the vault directly.
    KnowledgeVault& vault() { return vault_; }

private:
    KnowledgeVault vault_;
    ConsolidationEngine consolidator_;
    uint64_t id_counter_ = 0;
};

}  // namespace sqa::a1fs
