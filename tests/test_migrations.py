"""Tests for the database migration/versioning system."""
import pytest
from backend.infrastructure.migrations import MigrationRunner, migrations


def test_migration_runner_upgrade():
    """Documents are upgraded through the migration chain."""
    runner = MigrationRunner()

    @runner.register(version=1, description="Add color")
    def v1(doc):
        doc["color"] = "blue"
        return doc

    @runner.register(version=2, description="Add size")
    def v2(doc):
        doc["size"] = "large"
        return doc

    doc = {"id": "test-1", "name": "widget"}
    upgraded = runner.upgrade(doc)

    assert upgraded["color"] == "blue"
    assert upgraded["size"] == "large"
    assert upgraded["_schema_version"] == 2


def test_migration_skips_already_applied():
    """Documents at current version are not re-migrated."""
    runner = MigrationRunner()

    @runner.register(version=1, description="v1")
    def v1(doc):
        doc["v1_applied"] = True
        return doc

    doc = {"id": "test-2", "_schema_version": 1}
    upgraded = runner.upgrade(doc)
    assert "v1_applied" not in upgraded  # Should skip v1


def test_migration_partial_upgrade():
    """Documents at an intermediate version only get remaining migrations."""
    runner = MigrationRunner()

    @runner.register(version=1, description="v1")
    def v1(doc):
        doc["v1"] = True
        return doc

    @runner.register(version=2, description="v2")
    def v2(doc):
        doc["v2"] = True
        return doc

    @runner.register(version=3, description="v3")
    def v3(doc):
        doc["v3"] = True
        return doc

    doc = {"id": "test-3", "_schema_version": 1}
    upgraded = runner.upgrade(doc)
    assert "v1" not in upgraded  # Already past v1
    assert upgraded["v2"] is True
    assert upgraded["v3"] is True
    assert upgraded["_schema_version"] == 3


def test_global_migrations_status():
    """Global migrations instance reports status correctly."""
    status = migrations.status()
    assert status["total_migrations"] >= 4
    assert status["current_version"] >= 4
    assert isinstance(status["migrations"], list)


def test_global_migrations_upgrade_legacy_doc():
    """Global migrations handle a legacy document without schema version."""
    doc = {"id": "legacy-1", "text": "old doc", "vec": [1.0, 2.0]}
    upgraded = migrations.upgrade(doc)

    assert upgraded["tag"] == "untagged"       # v1: added tag
    assert "vec" not in upgraded               # v2: renamed to vector
    assert upgraded["vector"] == [1.0, 2.0]    # v2: vec -> vector
    assert "metadata" in upgraded              # v3: added metadata
    assert "created_at" in upgraded            # v4: added created_at
    assert upgraded["_schema_version"] == 4


def test_pending_migrations():
    """Pending migrations are reported correctly."""
    pending = migrations.pending(doc_version=0)
    assert len(pending) >= 4

    pending_from_2 = migrations.pending(doc_version=2)
    assert len(pending_from_2) >= 2
    assert all(m.version > 2 for m in pending_from_2)
