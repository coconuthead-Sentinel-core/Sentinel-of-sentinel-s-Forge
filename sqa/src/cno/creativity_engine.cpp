#include "creativity_engine.h"
#include <algorithm>
#include <unordered_set>

namespace sqa::cno {

CreativityEngine::CreativityEngine()
    : rng_(std::random_device{}()) {}

double CreativityEngine::score(const std::vector<std::string>& tags,
                               const std::string& intent_label,
                               double novelty) const {
    // Cross-domain tags (tags from different domains) boost creativity.
    std::unordered_set<std::string> domains;
    for (const auto& t : tags) {
        auto dot = t.find('.');
        if (dot != std::string::npos) {
            domains.insert(t.substr(0, dot));
        } else {
            domains.insert(t);
        }
    }
    double diversity = std::min(1.0, static_cast<double>(domains.size()) / 3.0);

    // Unknown intents get a novelty boost.
    double intent_novelty = (intent_label == "unknown") ? 0.5 : 0.0;

    double raw = 0.4 * novelty + 0.3 * diversity + 0.3 * intent_novelty;
    return std::clamp(raw, 0.0, 1.0);
}

std::vector<SymbolicRule> CreativityEngine::suggest_rules(
        const std::map<std::string, int>& token_counts,
        const std::vector<SymbolicRule>& existing_rules,
        int limit) const {
    // Collect existing patterns.
    std::unordered_set<std::string> existing;
    for (const auto& r : existing_rules) {
        existing.insert(r.pattern);
    }

    // Sort tokens by frequency descending.
    std::vector<std::pair<std::string, int>> sorted(token_counts.begin(),
                                                     token_counts.end());
    std::sort(sorted.begin(), sorted.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });

    std::vector<SymbolicRule> suggestions;
    for (const auto& [token, count] : sorted) {
        if (static_cast<int>(suggestions.size()) >= limit) break;
        if (existing.count(token)) continue;
        if (token.size() <= 2) continue;
        // Only suggest alphabetic tokens.
        bool alpha = std::all_of(token.begin(), token.end(),
                                  [](unsigned char c) { return std::isalpha(c); });
        if (!alpha) continue;
        suggestions.push_back({token, "tag:auto." + token});
    }
    return suggestions;
}

}  // namespace sqa::cno
