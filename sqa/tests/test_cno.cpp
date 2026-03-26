#include <gtest/gtest.h>
#include "cno/cognitive_neural_overlay.h"

using namespace sqa;
using namespace sqa::cno;

TEST(SymbolicProcessor, DefaultRulesTagError) {
    SymbolicProcessor sp;
    auto tags = sp.process("there was an error in the system");
    bool found = false;
    for (const auto& t : tags) {
        if (t == "tag:anomaly") found = true;
    }
    EXPECT_TRUE(found);
}

TEST(SymbolicProcessor, NoMatchReturnsEmpty) {
    SymbolicProcessor sp;
    auto tags = sp.process("hello world");
    EXPECT_TRUE(tags.empty());
}

TEST(SymbolicProcessor, CustomRules) {
    SymbolicProcessor sp;
    sp.set_rules({{"hello", "tag:greeting"}});
    auto tags = sp.process("hello world");
    ASSERT_EQ(tags.size(), 1u);
    EXPECT_EQ(tags[0], "tag:greeting");
}

TEST(AppraisalEngine, EvaluateReturnsDimensions) {
    AppraisalEngine ae;
    auto dims = ae.evaluate("happy joyful wonderful", {});
    double v = ae.valence(dims);
    EXPECT_GE(v, -1.0);
    EXPECT_LE(v, 1.0);
}

TEST(AppraisalEngine, NegativeValence) {
    AppraisalEngine ae;
    auto dims = ae.evaluate("terrible horrible awful", {});
    double v = ae.valence(dims);
    EXPECT_LT(v, 0.0);
}

TEST(AttentionModule, WeightRange) {
    AttentionModule am;
    double w = am.compute(0.8, 0.5, 0.7);
    EXPECT_GE(w, 0.0);
    EXPECT_LE(w, 1.0);
}

TEST(CreativityEngine, ScoreRange) {
    CreativityEngine ce;
    double s = ce.score({"tag:anomaly", "tag:domain.quantum"}, "query", 0.5);
    EXPECT_GE(s, 0.0);
    EXPECT_LE(s, 1.0);
}

TEST(CognitiveNeuralOverlay, ProcessReturnsSnapshot) {
    CognitiveNeuralOverlay cno;
    CognitiveInput inp;
    inp.id = "test_001";
    inp.text = "quantum error detected in system";
    auto snap = cno.process(inp);
    EXPECT_EQ(snap.id, "test_001");
    EXPECT_FALSE(snap.symbolic_tags.empty());
    EXPECT_GT(snap.processing_ms, 0.0);
}

TEST(CognitiveNeuralOverlay, ConfigureDoesNotCrash) {
    CognitiveNeuralOverlay cno;
    json cfg = {
        {"appraisalEngine", {{"enable", true}}},
        {"symbolicRules", json::array({
            {{"pattern", "test"}, {"tag", "tag:test"}}
        })}
    };
    EXPECT_NO_THROW(cno.configure(cfg));

    CognitiveInput inp;
    inp.id = "cfg_test";
    inp.text = "this is a test";
    auto snap = cno.process(inp);
    bool found = false;
    for (const auto& t : snap.symbolic_tags) {
        if (t == "tag:test") found = true;
    }
    EXPECT_TRUE(found);
}

TEST(CognitiveNeuralOverlay, ExecutionCount) {
    CognitiveNeuralOverlay cno;
    EXPECT_EQ(cno.executions(), 0u);
    CognitiveInput inp;
    inp.id = "x";
    inp.text = "hello";
    cno.process(inp);
    cno.process(inp);
    EXPECT_EQ(cno.executions(), 2u);
}
