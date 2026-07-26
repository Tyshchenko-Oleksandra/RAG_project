from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer_question, get_available_subjects

app = FastAPI()


class QuestionRequest(BaseModel):
    subject: str
    question: str


@app.get("/")
def home():
    return {
        "message": "University RAG API is running"
    }



@app.get("/subjects")
def get_subjects():
    subjects = get_available_subjects()
    return {"subjects": subjects}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = answer_question(
        question=request.question,
        subject=request.subject
    )

    return result

