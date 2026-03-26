#pragma once
#include "../common.h"
#include <cmath>
#include <unordered_set>

namespace sqa::cno {

/// Emotional appraisal engine based on Scherer/Smith-Lazarus Appraisal Theory.
/// Evaluates input along five dimensions and produces a valence score.
class AppraisalEngine {
public:
    AppraisalEngine();

    /// Configure dimension weights via JSON.
    void configure(const json& cfg);

    /// Evaluate text and return appraisal dimensions + composite valence.
    AppraisalDimensions evaluate(const std::string& text,
                                 const std::vector<std::string>& tags) const;

    /// Compute composite valence from dimensions: [-1, 1].
    double valence(const AppraisalDimensions& dims) const;

private:
    double w_novelty_    = 0.8;
    double w_relevance_  = 1.0;
    double w_congruence_ = 1.0;
    double w_agency_     = 0.5;
    double w_coping_     = 0.7;

    // Lexicons for quick valence estimation.
    std::unordered_set<std::string> positive_;
    std::unordered_set<std::string> negative_;
    std::unordered_set<std::string> novel_;
};

}  // namespace sqa::cno
