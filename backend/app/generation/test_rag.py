from backend.app.generation.rag_service import answer_question


if __name__ == "__main__":
    question = "Who approves purchase orders above 50000 dollars?"

    response = answer_question(question, top_k=3)

    print("\nQuestion:")
    print(response["question"])

    print("\nAnswer:")
    print(response["answer"])

    print("\nSources:")
    for source in response["sources"]:
        print(source)