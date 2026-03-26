#include "processing_node.h"
#include <chrono>

namespace sqa::nns {

ProcessingNode::ProcessingNode(Id id, TaskFn fn)
    : id_(std::move(id)), fn_(std::move(fn)) {}

TaskResult ProcessingNode::execute(const json& input) {
    auto start = Clock::now();
    ++executions_;
    TaskResult result;
    try {
        result = fn_(input);
    } catch (const std::exception& e) {
        result.success = false;
        result.error = e.what();
    }
    auto end = Clock::now();
    result.duration_ms = std::chrono::duration<double, std::milli>(end - start).count();
    result.task_id = id_;
    return result;
}

}  // namespace sqa::nns
