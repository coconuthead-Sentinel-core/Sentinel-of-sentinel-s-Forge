#pragma once
#include "../common.h"

namespace sqa::cno {

/// Attention allocation module.
/// Computes a weight [0,1] indicating how much cognitive resource to allocate.
class AttentionModule {
public:
    /// Compute attention weight from appraisal + intent score.
    double compute(double intent_score, double appraisal_valence,
                   double novelty) const;
};

}  // namespace sqa::cno
