import logging
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from backend.core.config import settings

logger = logging.getLogger(__name__)

# Default SQLite path — next to the app root so data survives restarts.
_DEFAULT_SQLITE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users.db"


class UserRepository:
    """Repository for user persistence.

    Priority order:
      1. Azure Cosmos DB (if credentials are configured)
      2. SQLite file (default — survives server restarts)
    """

    def __init__(self, sqlite_path: Optional[Path] = None):
        self._initialized = False
        self._mock_mode = False
        self._use_sqlite = False
        self._client = None
        self._container = None
        self._sqlite_path = sqlite_path or _DEFAULT_SQLITE_PATH
        self._sqlite_conn: Optional[sqlite3.Connection] = None
        self._sqlite_lock = threading.Lock()
        # Legacy in-memory fallback (only used in tests via clear_local_cache)
        self._users: dict[str, dict[str, Any]] = {}
        self._email_index: dict[str, str] = {}

    # ------------------------------------------------------------------
    # SQLite helpers
    # ------------------------------------------------------------------

    def _init_sqlite(self) -> None:
        """Open (or create) the SQLite database and ensure the schema exists."""
        self._sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self._sqlite_conn = sqlite3.connect(
            str(self._sqlite_path),
            check_same_thread=False,
        )
        self._sqlite_conn.row_factory = sqlite3.Row
        self._sqlite_conn.execute("PRAGMA journal_mode=WAL")
        self._sqlite_conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL DEFAULT 'user',
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                hashed_password TEXT NOT NULL,
                display_name TEXT NOT NULL DEFAULT '',
                role TEXT NOT NULL DEFAULT 'user',
                created_at TEXT NOT NULL,
                subscription_tier TEXT NOT NULL DEFAULT 'free',
                stripe_customer_id TEXT NOT NULL DEFAULT ''
            )
            """
        )
        self._sqlite_conn.commit()
        logger.info("SQLite user repository initialized at %s", self._sqlite_path)

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        return dict(row)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        # Try Cosmos DB first
        if settings.COSMOS_ENDPOINT and settings.COSMOS_KEY:
            try:
                from azure.cosmos import CosmosClient, PartitionKey

                self._client = CosmosClient(settings.COSMOS_ENDPOINT, credential=settings.COSMOS_KEY)
                database = self._client.create_database_if_not_exists(id=settings.COSMOS_DATABASE_NAME)
                self._container = database.create_container_if_not_exists(
                    id=settings.COSMOS_USER_CONTAINER_NAME,
                    partition_key=PartitionKey(path="/email"),
                )
                logger.info(
                    "Cosmos user repository initialized with container '%s'.",
                    settings.COSMOS_USER_CONTAINER_NAME,
                )
                return
            except Exception as exc:
                logger.warning("Cosmos user repository unavailable (%s). Falling back to SQLite.", exc)

        # Fall back to SQLite (persistent across restarts)
        try:
            self._init_sqlite()
            self._use_sqlite = True
            return
        except Exception as exc:
            logger.warning("SQLite init failed (%s). Using in-memory fallback.", exc)
            self._mock_mode = True

    def close(self) -> None:
        if self._client:
            self._client = None
        self._container = None
        if self._sqlite_conn:
            self._sqlite_conn.close()
            self._sqlite_conn = None
        self._use_sqlite = False
        self._initialized = False

    @property
    def is_mock_mode(self) -> bool:
        return self._mock_mode

    @property
    def is_sqlite_mode(self) -> bool:
        return self._use_sqlite

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def create_user(self, user_doc: dict[str, Any]) -> None:
        self.initialize()
        email = str(user_doc["email"]).lower().strip()
        user_doc["email"] = email
        user_doc.setdefault("type", "user")
        user_doc.setdefault("created_at", datetime.now(timezone.utc).isoformat())

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        # --- Cosmos DB ---
        if not self._mock_mode and not self._use_sqlite and self._container:
            self._container.create_item(body=user_doc)
            return

        # --- SQLite ---
        if self._use_sqlite and self._sqlite_conn:
            with self._sqlite_lock:
                self._sqlite_conn.execute(
                    """
                    INSERT INTO users (id, type, email, hashed_password, display_name,
                                       role, created_at, subscription_tier, stripe_customer_id)
                    VALUES (:id, :type, :email, :hashed_password, :display_name,
                            :role, :created_at, :subscription_tier, :stripe_customer_id)
                    """,
                    {
                        "id": user_doc["id"],
                        "type": user_doc.get("type", "user"),
                        "email": email,
                        "hashed_password": user_doc["hashed_password"],
                        "display_name": user_doc.get("display_name", ""),
                        "role": user_doc.get("role", "user"),
                        "created_at": user_doc.get("created_at", ""),
                        "subscription_tier": user_doc.get("subscription_tier", "free"),
                        "stripe_customer_id": user_doc.get("stripe_customer_id", ""),
                    },
                )
                self._sqlite_conn.commit()
            return

        # --- In-memory fallback ---
        self._users[user_doc["id"]] = user_doc.copy()
        self._email_index[email] = user_doc["id"]

    def get_user_by_email(self, email: str) -> Optional[dict[str, Any]]:
        self.initialize()
        email_lower = email.lower().strip()

        # --- Cosmos DB ---
        if not self._mock_mode and not self._use_sqlite and self._container:
            query = "SELECT TOP 1 * FROM c WHERE c.type = @type AND c.email = @email"
            params = [
                {"name": "@type", "value": "user"},
                {"name": "@email", "value": email_lower},
            ]
            items = list(
                self._container.query_items(
                    query=query,
                    parameters=params,
                    partition_key=email_lower,
                )
            )
            return items[0] if items else None

        # --- SQLite ---
        if self._use_sqlite and self._sqlite_conn:
            with self._sqlite_lock:
                cur = self._sqlite_conn.execute(
                    "SELECT * FROM users WHERE email = ? LIMIT 1",
                    (email_lower,),
                )
                row = cur.fetchone()
            return self._row_to_dict(row) if row else None

        # --- In-memory ---
        user_id = self._email_index.get(email_lower)
        return self._users.get(user_id) if user_id else None

    def get_user_by_id(self, user_id: str) -> Optional[dict[str, Any]]:
        self.initialize()

        # --- Cosmos DB ---
        if not self._mock_mode and not self._use_sqlite and self._container:
            query = "SELECT TOP 1 * FROM c WHERE c.type = @type AND c.id = @id"
            params = [
                {"name": "@type", "value": "user"},
                {"name": "@id", "value": user_id},
            ]
            items = list(
                self._container.query_items(
                    query=query,
                    parameters=params,
                    enable_cross_partition_query=True,
                )
            )
            return items[0] if items else None

        # --- SQLite ---
        if self._use_sqlite and self._sqlite_conn:
            with self._sqlite_lock:
                cur = self._sqlite_conn.execute(
                    "SELECT * FROM users WHERE id = ? LIMIT 1",
                    (user_id,),
                )
                row = cur.fetchone()
            return self._row_to_dict(row) if row else None

        # --- In-memory ---
        return self._users.get(user_id)

    def update_subscription(self, user_id: str, tier: str, stripe_customer_id: str = "") -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user["subscription_tier"] = tier
        if stripe_customer_id:
            user["stripe_customer_id"] = stripe_customer_id

        # --- Cosmos DB ---
        if not self._mock_mode and not self._use_sqlite and self._container:
            self._container.upsert_item(body=user)
            return True

        # --- SQLite ---
        if self._use_sqlite and self._sqlite_conn:
            with self._sqlite_lock:
                self._sqlite_conn.execute(
                    """
                    UPDATE users
                    SET subscription_tier = ?, stripe_customer_id = ?
                    WHERE id = ?
                    """,
                    (tier, stripe_customer_id or user.get("stripe_customer_id", ""), user_id),
                )
                self._sqlite_conn.commit()
            return True

        # --- In-memory ---
        self._users[user_id] = user
        self._email_index[user["email"]] = user_id
        return True

    def clear_local_cache(self) -> None:
        """Test helper to clear local fallback storage."""
        self._users.clear()
        self._email_index.clear()
        if self._use_sqlite and self._sqlite_conn:
            with self._sqlite_lock:
                self._sqlite_conn.execute("DELETE FROM users")
                self._sqlite_conn.commit()


user_repository = UserRepository()
