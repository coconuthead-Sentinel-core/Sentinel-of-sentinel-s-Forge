#include "nexus_node_stack.h"
#include <algorithm>

namespace sqa::nns {

NexusNodeStack::NexusNodeStack() {
    spdlog::debug("NNS initialized");
}

void NexusNodeStack::configure(const json& cfg) {
    if (cfg.contains("maxFeedbackIterations")) {
        feedback_.set_max_iterations(cfg["maxFeedbackIterations"].get<int>());
    }
}

void NexusNodeStack::add_node(ProcessingNode node) {
    std::lock_guard lock(mutex_);
    nodes_.push_back(std::move(node));
}

std::vector<TaskResult> NexusNodeStack::execute(const json& input, bool parallel) {
    std::lock_guard lock(mutex_);
    ++total_executions_;

    std::vector<TaskResult> results(nodes_.size());

    auto run_nodes = [&](const std::vector<size_t>& indices) {
        if (parallel && indices.size() > 1) {
            std::vector<std::thread> threads;
            for (size_t idx : indices) {
                threads.emplace_back([&, idx]() {
                    results[idx] = nodes_[idx].execute(input);
                });
            }
            for (auto& t : threads) t.join();
        } else {
            for (size_t idx : indices) {
                results[idx] = nodes_[idx].execute(input);
            }
        }
    };

    // Initial run: all nodes.
    std::vector<size_t> all_indices;
    for (size_t i = 0; i < nodes_.size(); ++i) all_indices.push_back(i);
    run_nodes(all_indices);

    // Feedback loop: re-run failed nodes.
    for (int iter = 0; iter < feedback_.max_iterations(); ++iter) {
        auto retry_ids = feedback_.evaluate(results);
        if (retry_ids.empty()) break;

        std::vector<size_t> retry_indices;
        for (const auto& rid : retry_ids) {
            for (size_t i = 0; i < nodes_.size(); ++i) {
                if (nodes_[i].id() == rid) {
                    retry_indices.push_back(i);
                }
            }
        }
        if (retry_indices.empty()) break;

        spdlog::debug("NNS feedback iteration {}: retrying {} nodes",
                      iter + 1, retry_indices.size());
        run_nodes(retry_indices);
    }

    return results;
}

json NexusNodeStack::merge_results(const std::vector<TaskResult>& results) {
    json merged = json::object();
    merged["task_count"] = results.size();
    int successes = 0;
    double total_ms = 0.0;
    json outputs = json::object();

    for (const auto& r : results) {
        if (r.success) ++successes;
        total_ms += r.duration_ms;
        outputs[r.task_id] = r.output;
    }

    merged["successes"] = successes;
    merged["failures"] = static_cast<int>(results.size()) - successes;
    merged["total_duration_ms"] = total_ms;
    merged["outputs"] = outputs;
    return merged;
}

json NexusNodeStack::status() const {
    std::lock_guard lock(mutex_);
    json s;
    s["node_count"] = nodes_.size();
    s["total_executions"] = total_executions_;
    s["max_feedback_iterations"] = feedback_.max_iterations();
    json node_info = json::array();
    for (const auto& n : nodes_) {
        node_info.push_back({{"id", n.id()}, {"executions", n.executions()}});
    }
    s["nodes"] = node_info;
    return s;
}

}  // namespace sqa::nns
