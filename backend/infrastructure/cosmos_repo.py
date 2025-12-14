import logging
from typing import List, Optional, Any, Dict
from backend.core.config import settings
from backend.domain.models import Note

logger = logging.getLogger(__name__)

# Flag to track if we should use mock mode for the database
# Set to True by default - enables offline development without Cosmos DB
_mock_db_mode = False

class CosmosDBRepository:
    """
    Infrastructure layer for Azure Cosmos DB interactions.
    Handles mapping between Domain Models and DB Schema.
    """
    _client = None
    _container_proxy = None

    @classmethod
    async def initialize(cls):
        global _mock_db_mode
        
        # If mock mode is already forced, skip DB initialization
        if _mock_db_mode:
            logger.info("🔧 MOCK DB MODE enabled. Skipping Cosmos DB connection.")
            return
            
        if not settings.COSMOS_ENDPOINT or not settings.COSMOS_KEY:
            logger.warning("⚠️ Cosmos DB credentials missing. Running in MOCK DB MODE.")
            _mock_db_mode = True
            return

        try:
            from azure.cosmos.aio import CosmosClient
            cls._client = CosmosClient(settings.COSMOS_ENDPOINT, credential=settings.COSMOS_KEY)
            database = cls._client.get_database_client(settings.COSMOS_DATABASE_NAME)
            cls._container_proxy = database.get_container_client(settings.COSMOS_CONTAINER_NAME)
            logger.info(f"✅ Cosmos DB Repository initialized: {settings.COSMOS_CONTAINER_NAME}")
        except Exception as e:
            logger.warning(f"⚠️ Cosmos DB unavailable ({e}). Running in MOCK DB MODE.")
            _mock_db_mode = True

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()

    @classmethod
    async def upsert_note(cls, note: Note) -> Optional[Dict[str, Any]]:
        global _mock_db_mode
        if _mock_db_mode or not cls._container_proxy:
            # Return a mock success response
            logger.info(f"[MOCK DB] Upsert simulated for note id={note.id}")
            return {"id": note.id, "status": "mock_upserted"}

        try:
            item = note.model_dump()
            item["partitionKey"] = note.tag or "default"
            if note.vector:
                item["vec"] = note.vector
                del item["vector"]
            result = await cls._container_proxy.upsert_item(item)
            return result
        except Exception as e:
            # ANY failure = fall back to mock mode (DB not ready, container missing, etc)
            logger.warning(f"⚠️ Cosmos DB error: {type(e).__name__}. Switching to MOCK DB MODE.")
            _mock_db_mode = True
            return {"id": note.id, "status": "mock_upserted"}

    @classmethod
    async def get_all_notes(cls) -> List[Dict[str, Any]]:
        if _mock_db_mode or not cls._container_proxy:
            # Return empty list for mock mode
            logger.info("[MOCK DB] Returning empty notes list.")
            return []

        try:
            query = "SELECT * FROM c"
            items = []
            async for item in cls._container_proxy.query_items(
                query=query,
                enable_cross_partition_query=True
            ):
                items.append(item)
            return items
        except Exception as e:
            logger.error(f"Cosmos Query Error: {e}")
            return []

cosmos_repo = CosmosDBRepository
