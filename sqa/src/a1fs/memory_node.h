#pragma once
#include "../common.h"
#include <unordered_map>

namespace sqa::a1fs {

/// A single node in the knowledge graph.
struct MemoryNode {
    Id                        id;
    std::string               content;
    std::string               type        = "episodic";  // episodic | semantic | procedural
    TimePoint                 created     = Clock::now();
    TimePoint                 last_access = Clock::now();
    double                    activation  = 1.0;   // 0..1, decays over time
    double                    clarity     = 1.0;   // 0..1
    std::vector<std::string>  symbolic_tags;
    json                      metadata    = json::object();
};

/// Relationship type between memory nodes.
enum class RelationType {
    Causal,
    Temporal,
    Semantic,
    Associative,
};

inline std::string relation_to_string(RelationType r) {
    switch (r) {
        case RelationType::Causal:      return "causal";
        case RelationType::Temporal:    return "temporal";
        case RelationType::Semantic:    return "semantic";
        case RelationType::Associative: return "associative";
    }
    return "unknown";
}

/// An edge connecting two memory nodes.
struct RelationshipEdge {
    Id            source;
    Id            target;
    RelationType  type   = RelationType::Associative;
    double        weight = 1.0;
};

}  // namespace sqa::a1fs
