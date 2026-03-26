#include "attention_module.h"
#include <algorithm>
#include <cmath>

namespace sqa::cno {

double AttentionModule::compute(double intent_score, double appraisal_valence,
                                double novelty) const {
    // Attention is higher when intent is strong, novelty is high,
    // or emotional valence is extreme (positive or negative).
    double emotional_salience = std::abs(appraisal_valence);
    double raw = 0.4 * intent_score + 0.3 * novelty + 0.3 * emotional_salience;
    return std::clamp(raw, 0.0, 1.0);
}

}  // namespace sqa::cno
