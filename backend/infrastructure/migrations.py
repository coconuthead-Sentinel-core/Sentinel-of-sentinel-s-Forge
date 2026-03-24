"""
Database Migration/Versioning System for Cosmos DB (NoSQL).

Since Cosmos DB is schemaless, traditional SQL migrations don't apply.
Instead, this system tracks document schema versions and applies
transformations when reading older documents.

Key concepts:
- Each migration has a version number and a transform function
- Documents carry a `_schema_version` field
- On read, documents are upgraded through the migration chain
- Migration history is stored in a dedicated Cosmos container
"""
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class Migration:
    """A single migration step."""

    def __init__(
        self,
        version: int,
        description: str,
        transform: Callable[[dict], dict],
    ):
        self.version = version
        self.description = description
        self.transform = transform
        self.applied_at: Optional[str] = None


class MigrationRunner:
    """Manages and applies document schema migrations.

    Usage:
        runner = MigrationRunner()

        @runner.register(version=1, description="Add 'tag' field with default")
        def migrate_v1(doc: dict) -> dict:
            if "tag" not in doc:
                doc["tag"] = "untagged"
            return doc

        @runner.register(version=2, description="Rename 'vec' to 'vector'")
        def migrate_v2(doc: dict) -> dict:
            if "vec" in doc:
                doc["vector"] = doc.pop("vec")
            return doc

        # Apply migrations to a document
        upgraded_doc = runner.upgrade(doc)
    """

    CURRENT_VERSION = 0  # Will be set to max registered version

    def __init__(self):
        self._migrations: dict[int, Migration] = {}
        self._applied: set[int] = set()

    def register(self, version: int, description: str):
        """Decorator to register a migration function."""
        def decorator(func: Callable[[dict], dict]):
            migration = Migration(version=version, description=description, transform=func)
            self._migrations[version] = migration
            # Update current version to highest registered
            MigrationRunner.CURRENT_VERSION = max(
                MigrationRunner.CURRENT_VERSION,
                version,
            )
            return func
        return decorator

    def upgrade(self, document: dict) -> dict:
        """Upgrade a document through all applicable migrations.

        Documents without _schema_version are treated as version 0.
        """
        doc_version = document.get("_schema_version", 0)

        if doc_version >= MigrationRunner.CURRENT_VERSION:
            return document  # Already at latest

        # Apply migrations in order
        for version in sorted(self._migrations.keys()):
            if version > doc_version:
                migration = self._migrations[version]
                try:
                    document = migration.transform(document)
                    document["_schema_version"] = version
                    logger.debug(
                        "Migrated doc %s: v%d -> v%d (%s)",
                        document.get("id", "?"),
                        version - 1,
                        version,
                        migration.description,
                    )
                except Exception as e:
                    logger.error(
                        "Migration v%d failed for doc %s: %s",
                        version,
                        document.get("id", "?"),
                        e,
                    )
                    break  # Stop migrating on error

        return document

    def status(self) -> dict[str, Any]:
        """Return current migration status."""
        return {
            "current_version": MigrationRunner.CURRENT_VERSION,
            "total_migrations": len(self._migrations),
            "migrations": [
                {
                    "version": m.version,
                    "description": m.description,
                    "applied_at": m.applied_at,
                }
                for m in sorted(self._migrations.values(), key=lambda m: m.version)
            ],
        }

    def pending(self, doc_version: int = 0) -> list[Migration]:
        """Return migrations that haven't been applied to a given doc version."""
        return [
            m for m in sorted(self._migrations.values(), key=lambda m: m.version)
            if m.version > doc_version
        ]


# --- Global migration runner instance ---
migrations = MigrationRunner()


# --- Register Migrations ---
# Add new migrations here as the schema evolves.

@migrations.register(version=1, description="Ensure all documents have _schema_version and tag field")
def migrate_v1(doc: dict) -> dict:
    """Baseline: add schema version tracking and ensure tag field exists."""
    if "tag" not in doc:
        doc["tag"] = "untagged"
    return doc


@migrations.register(version=2, description="Normalize vector field name from 'vec' to 'vector'")
def migrate_v2(doc: dict) -> dict:
    """Rename legacy 'vec' field to 'vector'."""
    if "vec" in doc:
        doc["vector"] = doc.pop("vec")
    return doc


@migrations.register(version=3, description="Add metadata field if missing")
def migrate_v3(doc: dict) -> dict:
    """Ensure metadata dict exists on all documents."""
    if "metadata" not in doc:
        doc["metadata"] = {}
    return doc


@migrations.register(version=4, description="Add created_at timestamp if missing")
def migrate_v4(doc: dict) -> dict:
    """Ensure created_at is present."""
    if "created_at" not in doc:
        doc["created_at"] = datetime.now(timezone.utc).isoformat()
    return doc
