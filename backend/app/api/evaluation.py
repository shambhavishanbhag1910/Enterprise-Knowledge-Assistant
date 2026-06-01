from fastapi import APIRouter, HTTPException

from backend.app.evaluation.evaluate_rag import run_evaluation

router = APIRouter(prefix="/api", tags=["Evaluation"])


@router.post("/evaluate")
def evaluate_rag_pipeline():
    """
    Run RAG evaluation using golden question dataset.
    """
    try:
        evaluation_output = run_evaluation()
        return evaluation_output

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error while running evaluation: {str(error)}",
        )