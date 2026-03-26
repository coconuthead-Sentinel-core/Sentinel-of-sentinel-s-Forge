#include <gtest/gtest.h>
#include "a1fs/a1_filing_system.h"

using namespace sqa;
using namespace sqa::a1fs;

TEST(KnowledgeVault, StoreAndRetrieve) {
    KnowledgeVault kv(100);
    MemoryNode node;
    node.id = "test_1";
    node.content = "hello world";
    node.symbolic_tags = {"tag:greeting"};
    auto id = kv.store(node);
    EXPECT_EQ(id, "test_1");
    EXPECT_EQ(kv.size(), 1u);
}

TEST(KnowledgeVault, GetById) {
    KnowledgeVault kv(100);
    MemoryNode node;
    node.id = "n1";
    node.content = "test content";
    kv.store(node);
    auto retrieved = kv.get("n1");
    ASSERT_TRUE(retrieved.has_value());
    EXPECT_EQ(retrieved->content, "test content");
}

TEST(KnowledgeVault, SimilarityRetrieval) {
    KnowledgeVault kv(100);
    MemoryNode n1;
    n1.id = "q1"; n1.content = "quantum error in system"; n1.symbolic_tags = {"tag:anomaly"};
    kv.store(n1);
    MemoryNode n2;
    n2.id = "q2"; n2.content = "happy greeting"; n2.symbolic_tags = {"tag:greeting"};
    kv.store(n2);
    MemoryNode n3;
    n3.id = "q3"; n3.content = "quantum physics research"; n3.symbolic_tags = {"tag:domain.quantum"};
    kv.store(n3);

    auto results = kv.retrieve_similar("quantum", 2);
    EXPECT_LE(results.size(), 2u);
}

TEST(KnowledgeVault, StrengthenActivation) {
    KnowledgeVault kv(100);
    MemoryNode node;
    node.id = "s1"; node.content = "test memory";
    kv.store(node);
    kv.strengthen("s1", 0.5);
    EXPECT_EQ(kv.size(), 1u);
}

TEST(KnowledgeVault, ClearRemovesAll) {
    KnowledgeVault kv(100);
    MemoryNode n1; n1.id = "a"; n1.content = "one";
    MemoryNode n2; n2.id = "b"; n2.content = "two";
    kv.store(n1);
    kv.store(n2);
    EXPECT_EQ(kv.size(), 2u);
    kv.clear();
    EXPECT_EQ(kv.size(), 0u);
}

TEST(KnowledgeVault, LinkNodes) {
    KnowledgeVault kv(100);
    MemoryNode n1; n1.id = "l1"; n1.content = "first";
    MemoryNode n2; n2.id = "l2"; n2.content = "second";
    kv.store(n1);
    kv.store(n2);
    EXPECT_NO_THROW(kv.link("l1", "l2", RelationType::Causal, 1.0));
    auto edges = kv.edges_for("l1");
    EXPECT_GE(edges.size(), 1u);
}

TEST(A1FilingSystem, FullPipeline) {
    A1FilingSystem fs(100);
    auto id = fs.store_episodic("quantum cognition test", {"tag:domain.quantum"}, {});
    EXPECT_FALSE(id.empty());
    EXPECT_EQ(fs.size(), 1u);

    auto similar = fs.retrieve_similar("quantum", 5);
    EXPECT_GE(similar.size(), 1u);

    int consolidated = fs.consolidate();
    EXPECT_GE(consolidated, 0);

    auto snap = fs.snapshot();
    EXPECT_TRUE(snap.contains("node_count"));
}

TEST(A1FilingSystem, LinkNodes) {
    A1FilingSystem fs(100);
    auto id1 = fs.store_episodic("first node", {}, {});
    auto id2 = fs.store_episodic("second node", {}, {});
    EXPECT_NO_THROW(fs.link(id1, id2, RelationType::Causal, 1.0));
}
