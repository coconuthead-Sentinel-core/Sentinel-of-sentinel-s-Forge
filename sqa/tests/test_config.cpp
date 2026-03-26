#include <gtest/gtest.h>
#include "config_loader.h"

using namespace sqa;

TEST(ConfigLoader, DefaultConfigHasAllSections) {
    auto cfg = default_config();
    EXPECT_TRUE(cfg.contains("global"));
    EXPECT_TRUE(cfg.contains("cno"));
    EXPECT_TRUE(cfg.contains("a1fs"));
    EXPECT_TRUE(cfg.contains("nns"));
}

TEST(ConfigLoader, DefaultConfigVersion) {
    auto cfg = default_config();
    EXPECT_EQ(cfg["global"]["version"], "8.0.0");
}

TEST(ConfigLoader, DefaultCNOHasSymbolicRules) {
    auto cfg = default_config();
    auto rules = cfg["cno"]["symbolicRules"];
    EXPECT_GT(rules.size(), 0u);
    EXPECT_EQ(rules[0]["pattern"], "error");
    EXPECT_EQ(rules[0]["tag"], "tag:anomaly");
}

TEST(ConfigLoader, DefaultA1FSCapacity) {
    auto cfg = default_config();
    EXPECT_EQ(cfg["a1fs"]["capacity"], 1024);
}

TEST(ConfigLoader, DefaultNNSParallelNodes) {
    auto cfg = default_config();
    EXPECT_EQ(cfg["nns"]["parallelNodes"], 4);
}

TEST(ConfigLoader, LoadMissingFileReturnDefaults) {
    auto cfg = load_config("/nonexistent/path/config.json");
    EXPECT_TRUE(cfg.contains("global"));
    EXPECT_EQ(cfg["global"]["version"], "8.0.0");
}
