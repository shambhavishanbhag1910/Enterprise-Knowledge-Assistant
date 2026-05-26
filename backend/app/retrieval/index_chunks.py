import json
from pathlib import Path
from typing import List, Dict, Any

from backend.app.retrieval.embedding_model import embed_texts, get_embedding_dimension
from backend.app.retrieval.vector_store import create_collection_if_not_exists, upsert_chunks


def load_chunks(chunks_path: str) -> List[Dict[str, Any]]:
    """
    Load chunks from JSONL file.
    """
    path = Path(chunks_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {chunks_path}. "
            "Please run ingestion pipeline first."
        )

    chunks = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def index_chunks(
    chunks_path: str = "data/chunks/document_chunks.jsonl"
) -> None:
    """
    Full indexing pipeline:
    1. Load chunks
    2. Generate embeddings
    3. Create Qdrant collection
    4. Store vectors in Qdrant
    """
    print("Loading chunks...")
    chunks = load_chunks(chunks_path)

    if not chunks:
        raise ValueError("No chunks found for indexing.")

    print(f"Total chunks loaded: {len(chunks)}")

    texts = [chunk["chunk_text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = embed_texts(texts)

    vector_size = get_embedding_dimension()
    print(f"Embedding vector size: {vector_size}")

    print("Creating Qdrant collection if needed...")
    create_collection_if_not_exists(vector_size)

    print("Uploading vectors to Qdrant...")
    upsert_chunks(chunks, embeddings)

    print("Indexing completed successfully.")


if __name__ == "__main__":
    index_chunks()