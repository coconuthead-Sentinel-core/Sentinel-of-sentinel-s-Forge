#pragma once
/**
 * SQA v8.0 — Common types shared across CNO, A1FS, and NNS.
 */

#include <chrono>
#include <cstdint>
#include <map>
#include <string>
#include <variant>
#include <vector>
#include <nlohmann/json.hpp>

namespace sqa {

using json = nlohmann::json;
using Clock = std::chrono::steady_clock;
using TimePoint = Clock::time_point;

/// Unique identifier type.
using Id = std::string;

/// Generic value that can flow through the cognitive pipeline.
using Value = std::variant<std::string, double, int64_t, bool, json>;

/// Convert a Value to JSON for serialisation.
inline json value_to_json(const Value& v) {
    return std::visit([](auto&& arg) -> json { return arg; }, v);
}

/// A single token flowing through the cognitive pipeline.
struct CognitiveInput {
    Id          id;
    std::string text;
    json        metadata = json::object();
    TimePoint   created  = Clock::now();
};

/// Snapshot of cognitive state after processing.
struct CognitiveStateSnapshot {
    Id                            id;
    std::string                   intent_label;
    double                        intent_score    = 0.0;
    double                        appraisal_valence = 0.0;
    double                        attention_weight  = 1.0;
    double                        creativity_score  = 0.0;
    std::vector<std::string>      symbolic_tags;
    json                          metadata = json::object();
    double                        processing_ms = 0.0;
};

/// Appraisal dimensions (from Appraisal Theory — Scherer/Smith & Lazarus).
struct AppraisalDimensions {
    double novelty                = 0.0;   // 0..1
    double motivational_relevance = 0.0;   // 0..1
    double motivational_congruence = 0.0;  // -1..1
    double accountability         = 0.0;   // 0..1 (self vs other)
    double coping_potential       = 0.0;   // 0..1
};

/// Symbolic tag rule: keyword → tag.
struct SymbolicRule {
    std::string pattern;
    std::string tag;
};

}  // namespace sqa
