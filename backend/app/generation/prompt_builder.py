from typing import List, Dict, Any


def build_context(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Convert retrieved chunks into context for the LLM.
    """
    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"""
Source {index}
Document Name: {chunk.get("document_name")}
Chunk Number: {chunk.get("chunk_number")}
Similarity Score: {chunk.get("score")}

Text:
{chunk.get("chunk_text")}
"""
        )

    return "\n".join(context_parts)


def build_rag_prompt(question: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Build a strict RAG prompt so the model answers only from retrieved context.
    """
    context = build_context(retrieved_chunks)

    return f"""
You are an enterprise document Q&A assistant.

Your task is to answer the user's question using only the provided document context.

Rules:
1. Use only the provided context.
2. Do not use outside knowledge.
3. Do not invent policy details, numbers, dates, names, approvals, or limits.
4. If the answer is not available in the context, say:
   "I could not find this information in the available documents."
5. Always mention the source document name.
6. Keep the answer simple, professional, and business friendly.
7. Do not reveal internal reasoning or chain of thought.

User Question:
{question}

Retrieved Document Context:
{context}

Return your response in this format:

Answer:
<clear answer>

Sources:
- <document name and chunk number>

Confidence:
High / Medium / Low
"""