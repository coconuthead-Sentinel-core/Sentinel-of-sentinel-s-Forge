#include "a1_filing_system.h"
#include <spdlog/spdlog.h>

namespace sqa::a1fs {

A1FilingSystem::A1FilingSystem(size_t capacity)
    : vault_(capacity), consolidator_(vault_) {
    spdlog::debug("A1FS initialized (capacity={})", capacity);
}

void A1FilingSystem::configure(const json& cfg) {
    if (cfg.contains("capacity")) {
        // Can't resize in-place, but configure is for initial setup.
    }
    if (cfg.contains("consolidation")) {
        consolidator_.configure(cfg["consolidation"]);
    }
}

Id A1FilingSystem::store_episodic(const std::string& text,
                                   const std::vector<std::string>& tags,
                                   const json& metadata) {
    MemoryNode node;
    node.id = "mem_" + std::to_string(++id_counter_);
    node.content = text;
    node.type = "episodic";
    node.symbolic_tags = tags;
    node.metadata = metadata;
    return vault_.store(std::move(node));
}

std::vector<std::pair<Id, double>> A1FilingSystem::retrieve_similar(
        const std::string& query, int top_k) const {
    return vault_.retrieve_similar(query, top_k);
}

void A1FilingSystem::strengthen(const Id& id, double amount) {
    vault_.strengthen(id, amount);
}

void A1FilingSystem::link(const Id& source, const Id& target,
                           RelationType type, double weight) {
    vault_.link(source, target, type, weight);
}

int A1FilingSystem::consolidate() {
    return consolidator_.consolidate();
}

json A1FilingSystem::snapshot() const {
    return vault_.snapshot();
}

void A1FilingSystem::clear() {
    vault_.clear();
}

size_t A1FilingSystem::size() const {
    return vault_.size();
}

}  // namespace sqa::a1fs
