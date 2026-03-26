#include "symbolic_processor.h"
#include <algorithm>
#include <cctype>

namespace sqa::cno {

SymbolicProcessor::SymbolicProcessor() {
    // Default rules matching the Python SymbolicArray defaults.
    rules_ = {
        {"error",     "tag:anomaly"},
        {"stress",    "tag:load"},
        {"final",     "tag:validation"},
        {"quantum",   "tag:domain.quantum"},
        {"cognition", "tag:domain.cognition"},
    };
}

void SymbolicProcessor::set_rules(const std::vector<SymbolicRule>& rules) {
    rules_ = rules;
}

std::vector<SymbolicRule> SymbolicProcessor::get_rules() const {
    return rules_;
}

std::vector<std::string> SymbolicProcessor::process(const std::string& text) const {
    // Lowercase the input for case-insensitive matching.
    std::string lower(text.size(), '\0');
    std::transform(text.begin(), text.end(), lower.begin(),
                   [](unsigned char c) { return std::tolower(c); });

    std::vector<std::string> tags;
    for (const auto& rule : rules_) {
        if (lower.find(rule.pattern) != std::string::npos) {
            tags.push_back(rule.tag);
        }
    }
    std::sort(tags.begin(), tags.end());
    tags.erase(std::unique(tags.begin(), tags.end()), tags.end());
    return tags;
}

}  // namespace sqa::cno
