#pragma once
#include "knowledge_vault.h"

namespace sqa::a1fs {

/// Memory consolidation engine.
/// Periodically decays activation, archives weak memories,
/// and strengthens frequently-accessed ones.
class ConsolidationEngine {
public:
    explicit ConsolidationEngine(KnowledgeVault& vault);

    /// Configure from JSON.
    void configure(const json& cfg);

    /// Run one consolidation cycle: decay all nodes, prune weak ones.
    /// Returns number of nodes archived (removed).
    int consolidate();

private:
    KnowledgeVault& vault_;
    double decay_rate_       = 0.02;  // activation drop per cycle
    double archive_threshold_ = 0.05; // nodes below this get archived
};

}  // namespace sqa::a1fs
