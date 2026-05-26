import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()


def get_qdrant_client() -> QdrantClient:
    """
    Create Qdrant client.
    """
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    return QdrantClient(url=qdrant_url)


def get_collection_name() -> str:
    """
    Get collection name from environment variable.
    """
    return os.getenv("QDRANT_COLLECTION", "enterprise_documents")


def create_collection_if_not_exists(vector_size: int) -> None:
    """
    Create Qdrant collection if it does not already exist.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()

    if client.collection_exists(collection_name):
        print(f"Collection already exists: {collection_name}")
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    print(f"Collection created successfully: {collection_name}")


def upsert_chunks(
    chunks: List[Dict[str, Any]],
    embeddings: List[List[float]]
) -> None:
    """
    Insert or update chunk embeddings into Qdrant.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()

    points = []

    for index, chunk in enumerate(chunks):
        point = PointStruct(
            id=index + 1,
            vector=embeddings[index],
            payload={
                "chunk_id": chunk["chunk_id"],
                "document_name": chunk["document_name"],
                "source_path": chunk["source_path"],
                "file_type": chunk["file_type"],
                "chunk_number": chunk["chunk_number"],
                "chunk_text": chunk["chunk_text"],
            }
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"Inserted/updated {len(points)} chunks into Qdrant.")


def search_similar_chunks(
    query_embedding: List[float],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search similar chunks from Qdrant using the newer Query API.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()

    response = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        with_payload=True
    )

    final_results = []

    for result in response.points:
        final_results.append(
            {
                "score": result.score,
                "chunk_id": result.payload.get("chunk_id"),
                "document_name": result.payload.get("document_name"),
                "chunk_number": result.payload.get("chunk_number"),
                "chunk_text": result.payload.get("chunk_text"),
                "source_path": result.payload.get("source_path"),
            }
        )

    return final_results
    