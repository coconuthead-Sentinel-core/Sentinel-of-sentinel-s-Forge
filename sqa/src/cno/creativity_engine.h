#pragma once
#include "../common.h"
#include <random>

namespace sqa::cno {

/// Creativity engine that generates novel associations.
/// Produces a creativity score and optional suggested connections.
class CreativityEngine {
public:
    CreativityEngine();

    /// Score how "creative" a combination of tags and intent is.
    /// Returns [0, 1] where higher = more novel combination.
    double score(const std::vector<std::string>& tags,
                 const std::string& intent_label,
                 double novelty) const;

    /// Suggest new tag rules from frequent patterns (mirrors Metatron).
    std::vector<SymbolicRule> suggest_rules(
        const std::map<std::string, int>& token_counts,
        const std::vector<SymbolicRule>& existing_rules,
        int limit = 5) const;

private:
    mutable std::mt19937 rng_;
};

}  // namespace sqa::cno
