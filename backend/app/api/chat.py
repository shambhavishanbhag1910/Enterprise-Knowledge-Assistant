from fastapi import APIRouter, HTTPException

from backend.app.api.schemas import ChatRequest, ChatResponse
from backend.app.generation.rag_service import answer_question

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Enterprise document Q&A endpoint.
    """
    try:
        result = answer_question(
            question=request.question,
            top_k=request.top_k or 5
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error while generating answer: {str(error)}"
        )