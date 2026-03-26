#pragma once
#include "../common.h"
#include <unordered_map>
#include <algorithm>

namespace sqa::cno {

/// Rule-based symbolic tagger (mirrors SymbolicArray in Python).
class SymbolicProcessor {
public:
    SymbolicProcessor();

    void set_rules(const std::vector<SymbolicRule>& rules);
    std::vector<SymbolicRule> get_rules() const;

    /// Tag input text and return matching symbolic tags.
    std::vector<std::string> process(const std::string& text) const;

private:
    std::vector<SymbolicRule> rules_;
};

}  // namespace sqa::cno
