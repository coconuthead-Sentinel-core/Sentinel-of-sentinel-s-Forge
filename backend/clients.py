import logging
import os
from typing import Optional

from openai import AzureOpenAI
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Best Practice: Use a managed identity in production for secure, passwordless authentication.
# DefaultAzureCredential will automatically use your 'az login' credentials for local development.
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

# --- Azure OpenAI Client ---
# Best Practice: Initialize one client and reuse it throughout the application.
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
aoai_client: Optional[AzureOpenAI] = None
if AOAI_ENDPOINT:
    aoai_client = AzureOpenAI(
        api_version=os.getenv("AOAI_API_VERSION", "2024-08-01-preview"),
        azure_endpoint=AOAI_ENDPOINT,
        azure_ad_token_provider=token_provider,
    )
else:
    logging.warning("AOAI_ENDPOINT not set; Azure OpenAI client will be unavailable.")

# --- Azure Cosmos DB Client ---
# Best Practice: Initialize one client and reuse it.
# For local development with the emulator, you'd use COSMOS_KEY.
# For production on Azure, you would ideally use the credential object.
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY") # Used for local emulator or key-based auth

cosmos_client: Optional[CosmosClient] = None
container_client = None
if cosmos_endpoint:
    if "localhost" in cosmos_endpoint:
        # Local emulator connection
        cosmos_client = CosmosClient(url=cosmos_endpoint, credential=cosmos_key)
    else:
        # Production connection using Managed Identity
        cosmos_client = CosmosClient(url=cosmos_endpoint, credential=credential)

    # Get database and container clients
    db_name = os.getenv("COSMOS_DATABASE_NAME")
    container_name = os.getenv("COSMOS_CONTAINER_NAME")
    if db_name and container_name:
        database_client = cosmos_client.get_database_client(db_name)
        container_client = database_client.get_container_client(container_name)
    else:
        logging.warning("COSMOS_DATABASE_NAME or COSMOS_CONTAINER_NAME not set; container client unavailable.")
else:
    logging.warning("COSMOS_ENDPOINT not set; Cosmos client will be unavailable.")

