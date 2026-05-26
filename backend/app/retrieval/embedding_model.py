import os
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load embedding model only once and reuse it.
    This avoids loading the model again and again for every request.
    """
    model_name = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5")
    return SentenceTransformer(model_name)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Convert list of text chunks into embedding vectors.
    """
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()


def get_embedding_dimension() -> int:
    """
    Find embedding vector size dynamically.
    This prevents hardcoding vector dimension.
    """
    sample_embedding = embed_texts(["sample text"])[0]
    return len(sample_embedding)