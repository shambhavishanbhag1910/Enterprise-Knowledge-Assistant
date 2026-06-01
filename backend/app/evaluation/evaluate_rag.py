import json
from pathlib import Path
from typing import Any, Dict, List

from backend.app.generation.rag_service import answer_question


DATASET_PATH = "data/golden_questions/rag_test_set.json"
RESULTS_PATH = "reports/evaluation/rag_eval_results.json"
SUMMARY_PATH = "reports/evaluation/rag_eval_summary.json"


def normalize_text(text: str) -> str:
    """
    Normalize text for simple comparison.
    """
    if not text:
        return ""

    return text.lower().replace(",", "").strip()


def calculate_keyword_score(answer: str, expected_keywords: List[str]) -> float:
    """
    Check how many expected keywords are present in the answer.
    """
    if not expected_keywords:
        return 0.0

    answer_normalized = normalize_text(answer)
    matched_count = 0

    for keyword in expected_keywords:
        keyword_normalized = normalize_text(keyword)

        if keyword_normalized in answer_normalized:
            matched_count += 1

    return matched_count / len(expected_keywords)


def calculate_source_match_score(
    retrieved_sources: List[Dict[str, Any]],
    expected_source: str,
) -> float:
    """
    Check whether expected source document is present in retrieved sources.
    """
    expected_source_normalized = normalize_text(expected_source)

    for source in retrieved_sources:
        document_name = normalize_text(source.get("document_name", ""))

        if document_name == expected_source_normalized:
            return 1.0

    return 0.0


def calculate_answer_present_score(answer: str) -> float:
    """
    Check whether answer was generated successfully.
    """
    answer_normalized = normalize_text(answer)

    if not answer_normalized:
        return 0.0

    if "could not find" in answer_normalized:
        return 0.0

    if "error" in answer_normalized:
        return 0.0

    return 1.0


def evaluate_question(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate one question against the RAG pipeline.
    """
    question = test_case["question"]
    expected_source = test_case["expected_source"]
    expected_keywords = test_case["expected_keywords"]

    rag_response = answer_question(question=question, top_k=3)

    answer = rag_response.get("answer", "")
    sources = rag_response.get("sources", [])

    keyword_score = calculate_keyword_score(
        answer=answer,
        expected_keywords=expected_keywords,
    )

    source_match_score = calculate_source_match_score(
        retrieved_sources=sources,
        expected_source=expected_source,
    )

    answer_present_score = calculate_answer_present_score(answer)

    overall_score = round(
        (keyword_score + source_match_score + answer_present_score) / 3,
        4,
    )

    return {
        "question": question,
        "expected_source": expected_source,
        "expected_keywords": expected_keywords,
        "answer": answer,
        "retrieved_sources": sources,
        "keyword_score": round(keyword_score, 4),
        "source_match_score": round(source_match_score, 4),
        "answer_present_score": round(answer_present_score, 4),
        "overall_score": overall_score,
    }


def run_evaluation() -> Dict[str, Any]:
    """
    Run evaluation for all golden questions.
    """
    dataset_file = Path(DATASET_PATH)

    if not dataset_file.exists():
        raise FileNotFoundError(f"Golden dataset not found: {DATASET_PATH}")

    with open(dataset_file, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    results = []

    for test_case in test_cases:
        print(f"Evaluating: {test_case['question']}")
        result = evaluate_question(test_case)
        results.append(result)

    total_questions = len(results)

    average_keyword_score = sum(item["keyword_score"] for item in results) / total_questions
    average_source_match_score = sum(item["source_match_score"] for item in results) / total_questions
    average_answer_present_score = sum(item["answer_present_score"] for item in results) / total_questions
    average_overall_score = sum(item["overall_score"] for item in results) / total_questions

    summary = {
        "total_questions": total_questions,
        "average_keyword_score": round(average_keyword_score, 4),
        "average_source_match_score": round(average_source_match_score, 4),
        "average_answer_present_score": round(average_answer_present_score, 4),
        "average_overall_score": round(average_overall_score, 4),
        "status": "PASS" if average_overall_score >= 0.75 else "FAIL",
    }

    Path(RESULTS_PATH).parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    with open(SUMMARY_PATH, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print("\nEvaluation completed.")
    print(f"Detailed results saved at: {RESULTS_PATH}")
    print(f"Summary saved at: {SUMMARY_PATH}")

    print("\nSummary:")
    print(json.dumps(summary, indent=4))

    return {
        "summary": summary,
        "results": results,
    }


if __name__ == "__main__":
    run_evaluation()