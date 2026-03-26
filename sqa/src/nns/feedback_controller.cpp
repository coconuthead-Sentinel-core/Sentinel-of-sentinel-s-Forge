#include "feedback_controller.h"

namespace sqa::nns {

std::vector<Id> FeedbackController::evaluate(
        const std::vector<TaskResult>& results) const {
    std::vector<Id> retry;
    for (const auto& r : results) {
        if (!r.success) {
            retry.push_back(r.task_id);
        }
    }
    return retry;
}

}  // namespace sqa::nns
