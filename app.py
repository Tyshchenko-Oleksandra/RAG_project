from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer_question

app = FastAPI()


class QuestionRequest(BaseModel):
    subject: str
    question: str


@app.get("/")
def home():
    return {
        "message": "University RAG API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = answer_question(
        question=request.question,
        subject=request.subject
    )

    return result