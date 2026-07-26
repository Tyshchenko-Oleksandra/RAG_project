from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="University Notes RAG API",
    description="API for asking questions based on university notes.",
    version="1.0.0"
)

app.include_router(router)