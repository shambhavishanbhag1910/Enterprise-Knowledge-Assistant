from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


class Source(BaseModel):
    document_name: str
    chunk_number: int
    score: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    retrieved_chunks: List[Dict[str, Any]]