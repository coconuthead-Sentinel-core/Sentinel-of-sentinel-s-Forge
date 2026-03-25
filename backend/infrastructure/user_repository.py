import logging
from datetime import datetime, timezone
from typing import Any, Optional

from backend.core.config import settings

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user persistence with Cosmos DB and local fallback."""

    def __init__(self):
        self._initialized = False
        self._mock_mode = False
        self._client = None
        self._container = None
        self._users: dict[str, dict[str, Any]] = {}
        self._email_index: dict[str, str] = {}

    def initialize(self) -> None:
        if self._initialized:
            return
        self._initialized = True

        if not settings.COSMOS_ENDPOINT or not settings.COSMOS_KEY:
            self._mock_mode = True
            logger.warning("Cosmos user repository credentials missing. Using in-memory fallback.")
            return

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
        except Exception as exc:
            logger.warning("Cosmos user repository unavailable (%s). Using in-memory fallback.", exc)
            self._mock_mode = True

    def close(self) -> None:
        if self._client:
            self._client = None
        self._container = None
        self._initialized = False

    @property
    def is_mock_mode(self) -> bool:
        return self._mock_mode

    def create_user(self, user_doc: dict[str, Any]) -> None:
        self.initialize()
        email = str(user_doc["email"]).lower().strip()
        user_doc["email"] = email
        user_doc.setdefault("type", "user")
        user_doc.setdefault("created_at", datetime.now(timezone.utc).isoformat())

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        if self._mock_mode or not self._container:
            self._users[user_doc["id"]] = user_doc.copy()
            self._email_index[email] = user_doc["id"]
            return

        self._container.create_item(body=user_doc)

    def get_user_by_email(self, email: str) -> Optional[dict[str, Any]]:
        self.initialize()
        email_lower = email.lower().strip()

        if self._mock_mode or not self._container:
            user_id = self._email_index.get(email_lower)
            return self._users.get(user_id) if user_id else None

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

    def get_user_by_id(self, user_id: str) -> Optional[dict[str, Any]]:
        self.initialize()

        if self._mock_mode or not self._container:
            return self._users.get(user_id)

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

    def update_subscription(self, user_id: str, tier: str, stripe_customer_id: str = "") -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user["subscription_tier"] = tier
        if stripe_customer_id:
            user["stripe_customer_id"] = stripe_customer_id

        if self._mock_mode or not self._container:
            self._users[user_id] = user
            self._email_index[user["email"]] = user_id
            return True

        self._container.upsert_item(body=user)
        return True

    def clear_local_cache(self) -> None:
        """Test helper to clear local fallback storage."""
        self._users.clear()
        self._email_index.clear()


user_repository = UserRepository()