#include "knowledge_vault.h"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <unordered_set>
#include <spdlog/spdlog.h>

namespace sqa::a1fs {

KnowledgeVault::KnowledgeVault(size_t capacity) : capacity_(capacity) {}

Id KnowledgeVault::store(MemoryNode node) {
    std::lock_guard lock(mutex_);
    if (nodes_.size() >= capacity_) {
        // Evict the lowest-activation node.
        Id lowest_id;
        double lowest_act = 2.0;
        for (const auto& [id, n] : nodes_) {
            if (n.activation < lowest_act) {
                lowest_act = n.activation;
                lowest_id = id;
            }
        }
        if (!lowest_id.empty()) {
            nodes_.erase(lowest_id);
            spdlog::debug("A1FS evicted node {}", lowest_id);
        }
    }
    Id id = node.id;
    nodes_[id] = std::move(node);
    spdlog::debug("A1FS stored node {} (total={})", id, nodes_.size());
    return id;
}

std::optional<MemoryNode> KnowledgeVault::get(const Id& id) const {
    std::lock_guard lock(mutex_);
    auto it = nodes_.find(id);
    if (it == nodes_.end()) return std::nullopt;
    return it->second;
}

std::vector<std::pair<Id, double>> KnowledgeVault::retrieve_similar(
        const std::string& query, int top_k) const {
    std::lock_guard lock(mutex_);
    std::vector<std::pair<Id, double>> scored;
    for (const auto& [id, node] : nodes_) {
        double sim = jaccard(query, node.content);
        // Boost by activation level.
        sim *= node.activation;
        scored.push_back({id, sim});
    }
    std::sort(scored.begin(), scored.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });
    if (static_cast<int>(scored.size()) > top_k) {
        scored.resize(static_cast<size_t>(top_k));
    }
    return scored;
}

void KnowledgeVault::strengthen(const Id& id, double amount) {
    std::lock_guard lock(mutex_);
    auto it = nodes_.find(id);
    if (it != nodes_.end()) {
        it->second.activation = std::min(1.0, it->second.activation + amount);
        it->second.last_access = Clock::now();
    }
}

void KnowledgeVault::link(const Id& source, const Id& target,
                           RelationType type, double weight) {
    std::lock_guard lock(mutex_);
    edges_.push_back({source, target, type, weight});
}

std::vector<RelationshipEdge> KnowledgeVault::edges_for(const Id& id) const {
    std::lock_guard lock(mutex_);
    std::vector<RelationshipEdge> result;
    for (const auto& e : edges_) {
        if (e.source == id || e.target == id) {
            result.push_back(e);
        }
    }
    return result;
}

size_t KnowledgeVault::size() const {
    std::lock_guard lock(mutex_);
    return nodes_.size();
}

json KnowledgeVault::snapshot() const {
    std::lock_guard lock(mutex_);
    json snap;
    snap["node_count"] = nodes_.size();
    snap["edge_count"] = edges_.size();
    snap["capacity"] = capacity_;
    json nodes_arr = json::array();
    for (const auto& [id, n] : nodes_) {
        nodes_arr.push_back({
            {"id", n.id},
            {"type", n.type},
            {"activation", n.activation},
            {"clarity", n.clarity},
            {"tags", n.symbolic_tags},
        });
    }
    snap["nodes"] = nodes_arr;
    return snap;
}

void KnowledgeVault::clear() {
    std::lock_guard lock(mutex_);
    nodes_.clear();
    edges_.clear();
}

double KnowledgeVault::jaccard(const std::string& a, const std::string& b) {
    auto tokenize = [](const std::string& s) {
        std::unordered_set<std::string> tokens;
        std::string lower(s.size(), '\0');
        std::transform(s.begin(), s.end(), lower.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        std::istringstream iss(lower);
        std::string w;
        while (iss >> w) tokens.insert(w);
        return tokens;
    };
    auto sa = tokenize(a);
    auto sb = tokenize(b);
    if (sa.empty() && sb.empty()) return 1.0;
    int inter = 0;
    for (const auto& t : sa) {
        if (sb.count(t)) ++inter;
    }
    int uni = static_cast<int>(sa.size() + sb.size()) - inter;
    return (uni > 0) ? static_cast<double>(inter) / uni : 0.0;
}

}  // namespace sqa::a1fs
