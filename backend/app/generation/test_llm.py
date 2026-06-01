from backend.app.generation.llm_client import generate_llm_answer


if __name__ == "__main__":
    prompt = "Explain RAG in one simple sentence."
    answer = generate_llm_answer(prompt)

    print("\nLLM Answer:")
    print(answer)