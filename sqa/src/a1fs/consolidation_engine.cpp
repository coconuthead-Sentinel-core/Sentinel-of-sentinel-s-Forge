#include "consolidation_engine.h"
#include <spdlog/spdlog.h>

namespace sqa::a1fs {

ConsolidationEngine::ConsolidationEngine(KnowledgeVault& vault)
    : vault_(vault) {}

void ConsolidationEngine::configure(const json& cfg) {
    if (cfg.contains("decayRate"))
        decay_rate_ = cfg["decayRate"].get<double>();
    if (cfg.contains("archiveThreshold"))
        archive_threshold_ = cfg["archiveThreshold"].get<double>();
}

int ConsolidationEngine::consolidate() {
    // Get snapshot to find IDs, then operate on vault.
    auto snap = vault_.snapshot();
    int archived = 0;

    if (!snap.contains("nodes") || !snap["nodes"].is_array()) return 0;

    // Decay activation for all nodes. If below threshold, archive.
    // We work by strengthening (negative = decay) or removing.
    std::vector<Id> to_remove;
    for (const auto& n : snap["nodes"]) {
        Id id = n["id"].get<std::string>();
        double act = n["activation"].get<double>();
        double new_act = act - decay_rate_;
        if (new_act <= archive_threshold_) {
            to_remove.push_back(id);
        } else {
            // Negative strengthen = decay.
            vault_.strengthen(id, -decay_rate_);
        }
    }

    // Note: KnowledgeVault doesn't expose remove() directly, so we
    // weaken archived nodes to near-zero — they'll be evicted on next store.
    for (const auto& id : to_remove) {
        vault_.strengthen(id, -(1.0));  // force to 0
        ++archived;
    }

    spdlog::debug("A1FS consolidation: decayed {} nodes, archived {}",
                  snap["nodes"].size(), archived);
    return archived;
}

}  // namespace sqa::a1fs
