"""
Document ingestion script for DefTech AI Document Assistant
Processes sample documents and loads them into vector database
"""
import os
from init_demo import init_cohere_client, init_qdrant_client
from document_processor import DocumentProcessor
from vector_store import VectorStore


def ingest_sample_documents():
    """
    Ingest all sample documents from the sample_docs directory
    """
    print("\n=== DefTech Document Ingestion ===\n")

    # Initialize clients
    cohere_client = init_cohere_client()
    qdrant_client = init_qdrant_client()

    # Initialize processor and vector store
    processor = DocumentProcessor(cohere_client)
    vector_store = VectorStore(qdrant_client)

    # Define sample documents to ingest
    documents = [
        {
            'file_path': './sample_docs/equipment_maintenance_manual.pdf',
            'manual_name': 'Equipment Maintenance Manual v3.2',
            'classification': 'UNCLASSIFIED',
            'document_type': 'manual',
            'metadata': {
                'manual_type': 'maintenance',
                'last_updated': '2024-01',
                'version': '3.2'
            }
        },
        {
            'file_path': './sample_docs/safety_guidelines.pdf',
            'manual_name': 'Safety Guidelines 2024',
            'classification': 'UNCLASSIFIED',
            'document_type': 'manual',
            'metadata': {
                'manual_type': 'safety',
                'last_updated': '2024-03',
                'version': '1.0'
            }
        },
        {
            'file_path': './sample_docs/tactical_doctrine.pdf',
            'manual_name': 'Tactical Doctrine TD-2023-04',
            'classification': 'SECRET',
            'document_type': 'doctrine',
            'metadata': {
                'doctrine_area': 'tactics',
                'last_updated': '2023-04',
                'version': 'TD-2023-04'
            }
        },
        {
            'file_path': './sample_docs/winter_operations.pdf',
            'manual_name': 'Winter Operations Procedures',
            'classification': 'UNCLASSIFIED',
            'document_type': 'manual',
            'metadata': {
                'manual_type': 'operations',
                'last_updated': '2024-02',
                'version': '2.1'
            }
        }
    ]

    total_chunks = 0

    for doc_info in documents:
        file_path = doc_info['file_path']

        # Check if file exists
        if not os.path.exists(file_path):
            print(f"⚠ File not found: {file_path}")
            print(f"  Skipping {doc_info['manual_name']}")
            continue

        print(f"\nProcessing: {doc_info['manual_name']}")
        print(f"  Classification: {doc_info['classification']}")
        print(f"  Type: {doc_info['document_type']}")

        # Process document into chunks
        chunks = processor.process_document(
            file_path=file_path,
            manual_name=doc_info['manual_name'],
            classification=doc_info['classification'],
            document_type=doc_info['document_type'],
            metadata=doc_info['metadata']
        )

        if not chunks:
            print(f"  ✗ No chunks generated")
            continue

        # Generate embeddings
        texts = [chunk['text'] for chunk in chunks]
        embeddings = processor.generate_embeddings(texts)

        if not embeddings:
            print(f"  ✗ Failed to generate embeddings")
            continue

        # Ingest into vector store
        vector_store.ingest_chunks(chunks, embeddings)
        total_chunks += len(chunks)

    # Print summary
    print("\n" + "=" * 50)
    print("Ingestion Complete")
    print("=" * 50)

    collection_info = vector_store.get_collection_info()
    print(f"\nCollection: {collection_info['name']}")
    print(f"Total chunks indexed: {collection_info['points_count']}")
    print(f"Status: {collection_info['status']}")
    print("\nReady to answer queries!\n")


if __name__ == "__main__":
    ingest_sample_documents()
