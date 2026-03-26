#include <gtest/gtest.h>
#include "nns/nexus_node_stack.h"

using namespace sqa;
using namespace sqa::nns;

TEST(ProcessingNode, BasicExecution) {
    ProcessingNode node("test_node", [](const json& input) -> TaskResult {
        TaskResult r;
        r.task_id = "test_node";
        r.success = true;
        r.output = {{"echo", input.value("msg", "none")}};
        return r;
    });
    json inp = {{"msg", "hello"}};
    auto result = node.execute(inp);
    EXPECT_TRUE(result.success);
    EXPECT_EQ(result.output["echo"], "hello");
}

TEST(ProcessingNode, FailingNode) {
    ProcessingNode node("fail_node", [](const json&) -> TaskResult {
        throw std::runtime_error("intentional failure");
    });
    json inp = {};
    auto result = node.execute(inp);
    EXPECT_FALSE(result.success);
    EXPECT_FALSE(result.error.empty());
}

TEST(FeedbackController, IdentifiesFailures) {
    FeedbackController fc;
    std::vector<TaskResult> results;

    TaskResult ok;
    ok.task_id = "ok_node";
    ok.success = true;
    results.push_back(ok);

    TaskResult fail;
    fail.task_id = "bad_node";
    fail.success = false;
    fail.error = "something went wrong";
    results.push_back(fail);

    auto retries = fc.evaluate(results);
    ASSERT_EQ(retries.size(), 1u);
    EXPECT_EQ(retries[0], "bad_node");
}

TEST(FeedbackController, AllSuccessNoRetries) {
    FeedbackController fc;
    std::vector<TaskResult> results;
    TaskResult ok;
    ok.task_id = "a";
    ok.success = true;
    results.push_back(ok);

    auto retries = fc.evaluate(results);
    EXPECT_TRUE(retries.empty());
}

TEST(NexusNodeStack, SequentialExecution) {
    NexusNodeStack nns;
    nns.add_node(ProcessingNode("n1", [](const json& inp) -> TaskResult {
        TaskResult r;
        r.task_id = "n1";
        r.success = true;
        r.output = {{"val", 42}};
        return r;
    }));

    json inp = {{"key", "value"}};
    auto results = nns.execute(inp, false); // sequential
    ASSERT_EQ(results.size(), 1u);
    EXPECT_TRUE(results[0].success);
}

TEST(NexusNodeStack, ParallelExecution) {
    NexusNodeStack nns;
    for (int i = 0; i < 4; ++i) {
        std::string id = "node_" + std::to_string(i);
        nns.add_node(ProcessingNode(id, [id](const json&) -> TaskResult {
            TaskResult r;
            r.task_id = id;
            r.success = true;
            r.output = {{"from", id}};
            return r;
        }));
    }

    json inp = {};
    auto results = nns.execute(inp, true); // parallel
    EXPECT_EQ(results.size(), 4u);
    for (const auto& r : results) {
        EXPECT_TRUE(r.success);
    }
}

TEST(NexusNodeStack, NodeCount) {
    NexusNodeStack nns;
    EXPECT_EQ(nns.node_count(), 0u);
    nns.add_node(ProcessingNode("a", [](const json&) -> TaskResult {
        return TaskResult{};
    }));
    EXPECT_EQ(nns.node_count(), 1u);
}

TEST(NexusNodeStack, StatusReport) {
    NexusNodeStack nns;
    auto s = nns.status();
    EXPECT_TRUE(s.contains("node_count"));
    EXPECT_EQ(s["node_count"], 0);
}

TEST(NexusNodeStack, MergeResults) {
    std::vector<TaskResult> results;
    TaskResult r1;
    r1.task_id = "a";
    r1.success = true;
    r1.output = {{"x", 1}};
    results.push_back(r1);

    TaskResult r2;
    r2.task_id = "b";
    r2.success = false;
    r2.error = "fail";
    results.push_back(r2);

    auto merged = NexusNodeStack::merge_results(results);
    EXPECT_EQ(merged["task_count"], 2);
    EXPECT_EQ(merged["successes"], 1);
    EXPECT_EQ(merged["failures"], 1);
}
