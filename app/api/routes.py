from fastapi import APIRouter, Depends

from app.api.dependencies import get_rag_service
from app.application.rag_service import RAGService
from app.schemas.schemas import QuestionRequest


router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "University RAG API is running"
    }


@router.get("/subjects")
def get_subjects(
    rag_service: RAGService = Depends(get_rag_service),
):
    return {
        "subjects": rag_service.get_subjects()
    }

@router.post("/ask")
def ask_question(
    request: QuestionRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    return rag_service.answer_question(
        question=request.question,
        subject=request.subject,
    )

    return result