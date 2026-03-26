#pragma once
/**
 * CognitiveNeuralOverlay — Central facade for the CNO subsystem.
 *
 * Routes input through: SymbolicProcessor → AppraisalEngine →
 * AttentionModule → CreativityEngine, producing a CognitiveStateSnapshot.
 */

#include "../common.h"
#include "symbolic_processor.h"
#include "appraisal_engine.h"
#include "attention_module.h"
#include "creativity_engine.h"
#include <spdlog/spdlog.h>

namespace sqa::cno {

class CognitiveNeuralOverlay {
public:
    CognitiveNeuralOverlay();

    /// Configure from JSON (loads sub-component configs).
    void configure(const json& cfg);

    /// Process a single input through the full CNO pipeline.
    CognitiveStateSnapshot process(const CognitiveInput& input);

    /// Access sub-components for management.
    SymbolicProcessor& symbolic()   { return symbolic_; }
    AppraisalEngine&   appraisal()  { return appraisal_; }
    CreativityEngine&  creativity() { return creativity_; }

    /// Return execution count.
    uint64_t executions() const { return executions_; }

private:
    SymbolicProcessor symbolic_;
    AppraisalEngine   appraisal_;
    AttentionModule   attention_;
    CreativityEngine  creativity_;

    uint64_t executions_ = 0;

    /// Simple keyword-based intent parsing (mirrors IntentParserNode).
    std::pair<std::string, double> parse_intent(const std::string& text) const;
};

}  // namespace sqa::cno
