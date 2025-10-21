"""
Vector store operations for DefTech AI Document Assistant
Handles Qdrant database interactions
"""
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import config


class VectorStore:
    """Manages vector database operations with Qdrant"""

    def __init__(self, qdrant_client: QdrantClient):
        self.client = qdrant_client
        self.collection_name = config.QDRANT_COLLECTION

    def ingest_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Ingest document chunks with embeddings into Qdrant

        Args:
            chunks: List of chunk metadata dictionaries
            embeddings: Corresponding embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())

            # Create point with vector and payload (metadata)
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    'text': chunk['text'],
                    'manual_name': chunk['manual_name'],
                    'page': chunk['page'],
                    'section': chunk['section'],
                    'classification': chunk['classification'],
                    'document_type': chunk['document_type'],
                    'last_updated': chunk.get('last_updated', '2024'),
                    # Add any additional metadata
                    **{k: v for k, v in chunk.items()
                       if k not in ['text', 'manual_name', 'page', 'section',
                                    'classification', 'document_type', 'last_updated']}
                }
            )
            points.append(point)

        # Batch upsert to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"✓ Ingested {len(points)} chunks into {self.collection_name}")

    def search(
        self,
        query_embedding: List[float],
        limit: int = None,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search vector database for similar chunks

        Args:
            query_embedding: Query vector
            limit: Maximum number of results (default from config)
            filters: Optional filters (e.g., {'document_type': 'manual'})

        Returns:
            List of search results with metadata and scores
        """
        if limit is None:
            limit = config.TOP_K_RESULTS

        # Build filter conditions if provided
        query_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            if conditions:
                query_filter = Filter(must=conditions)

        # Execute search
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=query_filter
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                'text': hit.payload['text'],
                'manual_name': hit.payload['manual_name'],
                'page': hit.payload['page'],
                'section': hit.payload['section'],
                'classification': hit.payload['classification'],
                'document_type': hit.payload['document_type'],
                'score': hit.score,
                'metadata': hit.payload
            })

        return results

    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        collection_info = self.client.get_collection(self.collection_name)

        return {
            'name': self.collection_name,
            'vectors_count': collection_info.vectors_count,
            'points_count': collection_info.points_count,
            'status': collection_info.status
        }

    def delete_collection(self):
        """Delete the entire collection (use with caution!)"""
        self.client.delete_collection(self.collection_name)
        print(f"✓ Deleted collection: {self.collection_name}")

    def search_by_manual_type(
        self,
        query_embedding: List[float],
        manual_type: str = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Search manuals with optional type filtering

        Args:
            query_embedding: Query vector
            manual_type: Optional manual type filter
            limit: Maximum results

        Returns:
            List of results
        """
        filters = {'document_type': 'manual'}

        if manual_type and manual_type in config.MANUAL_TYPES:
            filters['manual_type'] = manual_type

        return self.search(query_embedding, limit, filters)

    def search_by_doctrine_area(
        self,
        query_embedding: List[float],
        doctrine_area: str = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Search doctrine with optional area filtering

        Args:
            query_embedding: Query vector
            doctrine_area: Optional doctrine area filter
            limit: Maximum results

        Returns:
            List of results
        """
        filters = {'document_type': 'doctrine'}

        if doctrine_area and doctrine_area in config.DOCTRINE_AREAS:
            filters['doctrine_area'] = doctrine_area

        return self.search(query_embedding, limit, filters)


if __name__ == "__main__":
    # Test vector store
    from init_demo import init_qdrant_client

    qdrant_client = init_qdrant_client()
    vector_store = VectorStore(qdrant_client)

    info = vector_store.get_collection_info()
    print(f"\nCollection Info:")
    print(f"  Name: {info['name']}")
    print(f"  Points: {info['points_count']}")
    print(f"  Status: {info['status']}")
