from functools import lru_cache

from app.application.rag_service import RAGService
from app.core.factories import create_rag_service


@lru_cache
def get_rag_service() -> RAGService:
    return create_rag_service()