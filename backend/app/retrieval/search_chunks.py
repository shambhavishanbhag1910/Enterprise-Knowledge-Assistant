from backend.app.retrieval.embedding_model import embed_texts
from backend.app.retrieval.vector_store import search_similar_chunks


def search_documents(query: str, top_k: int = 5):
    """
    Search relevant document chunks for a user question.
    """
    query_embedding = embed_texts([query])[0]

    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=top_k
    )

    return results


if __name__ == "__main__":
    question = "Who approves purchase orders above 50000 dollars?"

    results = search_documents(question)

    print("\nUser Question:")
    print(question)

    print("\nTop Matching Chunks:")
    for index, result in enumerate(results, start=1):
        print("\n" + "=" * 80)
        print(f"Result: {index}")
        print(f"Score: {result['score']}")
        print(f"Document: {result['document_name']}")
        print(f"Chunk Number: {result['chunk_number']}")
        print(f"Text: {result['chunk_text']}")