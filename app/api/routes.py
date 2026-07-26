from fastapi import APIRouter

from app.models.schemas import QuestionRequest
from app.services.rag_service import answer_question
from app.services.vector_store_service import get_available_subjects


router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "University RAG API is running"
    }


@router.get("/subjects")
def get_subjects():
    subjects = get_available_subjects()
    return {
        "subjects": subjects
    }


@router.post("/ask")
def ask_question(request: QuestionRequest):
    result = answer_question(
        question=request.question,
        subject=request.subject
    )

    return result