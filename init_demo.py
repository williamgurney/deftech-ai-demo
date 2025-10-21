"""
Initialization script for DefTech AI Document Assistant Demo
Sets up Cohere client and Qdrant vector database
"""
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import config
import os


def init_cohere_client():
    """Initialize Cohere API client"""
    if not config.COHERE_API_KEY:
        raise ValueError(
            "COHERE_API_KEY not found. Please set it in your .env file or environment variables."
        )

    client = cohere.ClientV2(api_key=config.COHERE_API_KEY)
    print("✓ Cohere client initialized successfully")
    return client


def init_qdrant_client():
    """Initialize Qdrant vector database (local mode)"""
    # Create local Qdrant instance
    client = QdrantClient(path=config.QDRANT_PATH)

    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [col.name for col in collections]

    if config.QDRANT_COLLECTION not in collection_names:
        # Create collection with Cohere embedding dimensions
        client.create_collection(
            collection_name=config.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=config.EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
        print(f"✓ Created Qdrant collection: {config.QDRANT_COLLECTION}")
    else:
        print(f"✓ Qdrant collection already exists: {config.QDRANT_COLLECTION}")

    return client


def verify_setup():
    """Verify that all dependencies are properly configured"""
    print("\n=== DefTech AI Document Assistant - Setup Verification ===\n")

    try:
        # Test Cohere connection
        cohere_client = init_cohere_client()

        # Test Qdrant connection
        qdrant_client = init_qdrant_client()

        # Verify directories
        os.makedirs("./sample_docs", exist_ok=True)
        print("✓ Sample documents directory ready")

        os.makedirs(config.AUDIT_LOG_DIR, exist_ok=True)
        print("✓ Audit logs directory ready")

        print("\n=== Setup Complete ===")
        print("Ready to ingest documents and run queries!\n")

        return cohere_client, qdrant_client

    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        raise


if __name__ == "__main__":
    verify_setup()
