#include "cognitive_neural_overlay.h"
#include <algorithm>
#include <cctype>
#include <chrono>
#include <sstream>
#include <unordered_map>
#include <unordered_set>

namespace sqa::cno {

CognitiveNeuralOverlay::CognitiveNeuralOverlay() {
    spdlog::debug("CNO initialized");
}

void CognitiveNeuralOverlay::configure(const json& cfg) {
    if (cfg.contains("appraisalEngine")) {
        appraisal_.configure(cfg["appraisalEngine"]);
    }
    if (cfg.contains("symbolicRules")) {
        std::vector<SymbolicRule> rules;
        for (const auto& r : cfg["symbolicRules"]) {
            rules.push_back({r["pattern"].get<std::string>(),
                             r["tag"].get<std::string>()});
        }
        symbolic_.set_rules(rules);
    }
    spdlog::info("CNO configured from JSON");
}

CognitiveStateSnapshot CognitiveNeuralOverlay::process(const CognitiveInput& input) {
    auto start = Clock::now();
    ++executions_;

    CognitiveStateSnapshot snap;
    snap.id = input.id;
    snap.metadata = input.metadata;

    // 1. Symbolic tagging.
    snap.symbolic_tags = symbolic_.process(input.text);

    // 2. Intent parsing.
    auto [intent_label, intent_score] = parse_intent(input.text);
    snap.intent_label = intent_label;
    snap.intent_score = intent_score;

    // 3. Emotional appraisal.
    auto dims = appraisal_.evaluate(input.text, snap.symbolic_tags);
    snap.appraisal_valence = appraisal_.valence(dims);

    // 4. Attention allocation.
    snap.attention_weight = attention_.compute(
        intent_score, snap.appraisal_valence, dims.novelty);

    // 5. Creativity scoring.
    snap.creativity_score = creativity_.score(
        snap.symbolic_tags, intent_label, dims.novelty);

    auto end = Clock::now();
    snap.processing_ms = std::chrono::duration<double, std::milli>(end - start).count();

    spdlog::debug("CNO processed '{}' -> intent={} score={:.2f} valence={:.2f} in {:.3f}ms",
                  input.id, snap.intent_label, snap.intent_score,
                  snap.appraisal_valence, snap.processing_ms);

    return snap;
}

std::pair<std::string, double> CognitiveNeuralOverlay::parse_intent(
        const std::string& text) const {
    // Lowercase + tokenize.
    std::string lower(text.size(), '\0');
    std::transform(text.begin(), text.end(), lower.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    std::istringstream iss(lower);
    std::unordered_set<std::string> words;
    std::string w;
    while (iss >> w) words.insert(w);

    // Intent patterns mirroring IntentParserNode in Python.
    static const std::unordered_map<std::string,
                                     std::unordered_set<std::string>> patterns = {
        {"status",  {"status", "state", "health"}},
        {"help",    {"help", "assist", "how", "instructions"}},
        {"stress",  {"stress", "load", "benchmark", "throughput"}},
        {"upgrade", {"upgrade", "update", "improve"}},
        {"save",    {"save", "persist", "checkpoint"}},
        {"process", {"process", "run", "execute"}},
    };

    std::string best = "unknown";
    int best_hits = 0;
    for (const auto& [label, keys] : patterns) {
        int hits = 0;
        for (const auto& k : keys) {
            if (words.count(k)) ++hits;
        }
        if (hits > best_hits) {
            best = label;
            best_hits = hits;
        }
    }
    double score = (best_hits > 0) ? std::min(1.0, best_hits / 3.0) : 0.0;
    return {best, score};
}

}  // namespace sqa::cno
