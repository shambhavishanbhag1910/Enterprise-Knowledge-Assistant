from typing import Dict, Any

from langfuse import observe, propagate_attributes

from backend.app.retrieval.search_chunks import search_documents
from backend.app.generation.prompt_builder import build_rag_prompt
from backend.app.generation.llm_client import generate_llm_answer
from backend.app.observability.langfuse_client import flush_langfuse


@observe(name="rag_answer_question", as_type="span")
def answer_question(question: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Complete RAG flow with Langfuse tracing.
    """
    with propagate_attributes(
        trace_name="enterprise-rag-chat",
        user_id="demo_user",
        session_id="demo_session",
        tags=["rag", "enterprise-knowledge-assistant"],
        metadata={
            "project": "Enterprise Knowledge Assistant",
            "top_k": top_k,
        },
    ):
        retrieved_chunks = traced_search_documents(question, top_k)

        if not retrieved_chunks:
            result = {
                "question": question,
                "answer": "I could not find relevant information in the available documents.",
                "sources": [],
                "retrieved_chunks": [],
            }
            flush_langfuse()
            return result

        prompt = traced_build_prompt(question, retrieved_chunks)

        answer = traced_generate_answer(prompt)

        sources = [
            {
                "document_name": chunk.get("document_name"),
                "chunk_number": chunk.get("chunk_number"),
                "score": chunk.get("score"),
            }
            for chunk in retrieved_chunks
        ]

        result = {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieved_chunks": retrieved_chunks,
        }

        flush_langfuse()
        return result


@observe(name="qdrant_retrieval", as_type="retriever")
def traced_search_documents(question: str, top_k: int):
    return search_documents(question, top_k)


@observe(name="rag_prompt_builder", as_type="span")
def traced_build_prompt(question: str, retrieved_chunks):
    return build_rag_prompt(question, retrieved_chunks)


@observe(name="groq_llm_generation", as_type="generation")
def traced_generate_answer(prompt: str):
    return generate_llm_answer(prompt)