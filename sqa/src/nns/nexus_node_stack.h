#pragma once
/**
 * NexusNodeStack — Parallel task orchestrator with feedback loops.
 *
 * Breaks work into processing nodes, runs them (optionally in parallel),
 * merges results, and feeds failures back through the FeedbackController.
 */
#include "processing_node.h"
#include "feedback_controller.h"
#include <mutex>
#include <thread>
#include <vector>
#include <spdlog/spdlog.h>

namespace sqa::nns {

class NexusNodeStack {
public:
    NexusNodeStack();

    void configure(const json& cfg);

    /// Register a processing node.
    void add_node(ProcessingNode node);

    /// Execute all registered nodes against the input.
    /// If parallel=true, nodes run on separate threads.
    /// FeedbackController re-runs failed nodes up to max_iterations.
    std::vector<TaskResult> execute(const json& input, bool parallel = true);

    /// Merge multiple task results into a single JSON output.
    static json merge_results(const std::vector<TaskResult>& results);

    /// Node count.
    size_t node_count() const { return nodes_.size(); }

    /// Status snapshot.
    json status() const;

private:
    std::vector<ProcessingNode> nodes_;
    FeedbackController feedback_;
    mutable std::mutex mutex_;
    uint64_t total_executions_ = 0;
};

}  // namespace sqa::nns
