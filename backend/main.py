from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.observability import router as observability_router
from backend.app.api.chat import router as chat_router
from backend.app.api.evaluation import router as evaluation_router


app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="Enterprise Document Q&A Assistant using RAG, Qdrant, Sentence Transformers and Groq",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(evaluation_router)
app.include_router(observability_router)

@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }