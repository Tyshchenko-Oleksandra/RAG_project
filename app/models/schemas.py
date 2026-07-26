from pydantic import BaseModel


class QuestionRequest(BaseModel):
    subject: str
    question: str