#pragma once
#include "../common.h"
#include <functional>
#include <string>

namespace sqa::nns {

/// Result of a single task execution.
struct TaskResult {
    Id          task_id;
    bool        success = true;
    json        output  = json::object();
    double      duration_ms = 0.0;
    std::string error;
};

/// Abstract cognitive task — derived types implement execute().
class CognitiveTask {
public:
    explicit CognitiveTask(Id id, std::string type = "generic")
        : id_(std::move(id)), type_(std::move(type)) {}
    virtual ~CognitiveTask() = default;

    const Id& id()   const { return id_; }
    const std::string& type() const { return type_; }

    /// Execute the task and return a result.
    virtual TaskResult execute(const json& input) = 0;

private:
    Id id_;
    std::string type_;
};

/// A processing node that wraps a task function.
class ProcessingNode {
public:
    using TaskFn = std::function<TaskResult(const json&)>;

    ProcessingNode(Id id, TaskFn fn);

    TaskResult execute(const json& input);

    const Id& id() const { return id_; }
    uint64_t executions() const { return executions_; }

private:
    Id id_;
    TaskFn fn_;
    uint64_t executions_ = 0;
};

}  // namespace sqa::nns
