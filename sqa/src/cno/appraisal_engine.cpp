#include "appraisal_engine.h"
#include <algorithm>
#include <cctype>
#include <sstream>

namespace sqa::cno {

AppraisalEngine::AppraisalEngine() {
    positive_ = {"good", "great", "love", "happy", "win", "success",
                 "calm", "excellent", "brilliant", "perfect", "achieve"};
    negative_ = {"bad", "hate", "angry", "fail", "error", "stress",
                 "panic", "broken", "crash", "terrible", "awful"};
    novel_    = {"quantum", "forge", "nexus", "sentinel", "cognition",
                 "neural", "glyph", "metatron", "entropy", "lattice"};
}

void AppraisalEngine::configure(const json& cfg) {
    if (cfg.contains("weights")) {
        auto& w = cfg["weights"];
        if (w.contains("novelty"))    w_novelty_    = w["novelty"].get<double>();
        if (w.contains("relevance"))  w_relevance_  = w["relevance"].get<double>();
        if (w.contains("congruence")) w_congruence_ = w["congruence"].get<double>();
        if (w.contains("agency"))     w_agency_     = w["agency"].get<double>();
        if (w.contains("coping"))     w_coping_     = w["coping"].get<double>();
    }
}

AppraisalDimensions AppraisalEngine::evaluate(
        const std::string& text,
        const std::vector<std::string>& tags) const {

    // Tokenize to lowercase words.
    std::string lower(text.size(), '\0');
    std::transform(text.begin(), text.end(), lower.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    std::istringstream iss(lower);
    std::vector<std::string> words;
    std::string w;
    while (iss >> w) words.push_back(w);

    int pos = 0, neg = 0, nov = 0;
    for (const auto& word : words) {
        if (positive_.count(word)) ++pos;
        if (negative_.count(word)) ++neg;
        if (novel_.count(word))    ++nov;
    }
    int total = static_cast<int>(words.size());
    if (total == 0) total = 1;

    AppraisalDimensions dims;

    // Novelty: proportion of novel domain terms.
    dims.novelty = std::min(1.0, static_cast<double>(nov) / std::max(1, total / 3));

    // Motivational relevance: based on tag density (more tags = more relevant).
    dims.motivational_relevance = std::min(1.0, static_cast<double>(tags.size()) / 3.0);

    // Motivational congruence: positive vs negative sentiment [-1, 1].
    if (pos + neg > 0) {
        dims.motivational_congruence =
            static_cast<double>(pos - neg) / static_cast<double>(pos + neg);
    }

    // Accountability: self-reference heuristic.
    for (const auto& word : words) {
        if (word == "i" || word == "my" || word == "we" || word == "our") {
            dims.accountability = std::min(1.0, dims.accountability + 0.3);
        }
    }

    // Coping potential: inversely related to stress/negative indicators.
    dims.coping_potential = 1.0 - std::min(1.0, static_cast<double>(neg) / std::max(1, total / 4));

    return dims;
}

double AppraisalEngine::valence(const AppraisalDimensions& dims) const {
    double raw = w_novelty_    * dims.novelty
               + w_relevance_  * dims.motivational_relevance
               + w_congruence_ * dims.motivational_congruence
               + w_agency_     * dims.accountability
               + w_coping_     * dims.coping_potential;
    double sum_w = w_novelty_ + w_relevance_ + w_congruence_ + w_agency_ + w_coping_;
    if (sum_w == 0.0) return 0.0;
    return std::clamp(raw / sum_w, -1.0, 1.0);
}

}  // namespace sqa::cno
