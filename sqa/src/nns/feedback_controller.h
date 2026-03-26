#pragma once
#include "processing_node.h"
#include <vector>

namespace sqa::nns {

/// Controls feedback loops: decides whether to re-run tasks based on results.
class FeedbackController {
public:
    /// Evaluate results and return IDs of tasks that should be re-run.
    std::vector<Id> evaluate(const std::vector<TaskResult>& results) const;

    /// Set the maximum number of feedback iterations.
    void set_max_iterations(int max) { max_iterations_ = max; }
    int max_iterations() const { return max_iterations_; }

private:
    int max_iterations_ = 3;
};

}  // namespace sqa::nns
