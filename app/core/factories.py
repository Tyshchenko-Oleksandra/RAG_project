from app.application.rag_service import RAGService
from app.core.config import settings
from app.infrastructure.embeddings.openai_embedding_model import (
    OpenAIEmbeddingModel,
)
from app.infrastructure.llm.openai_chat_model import OpenAIChatModel
from app.infrastructure.vector_stores.chroma_notes_repository import (
    ChromaNotesRepository,
)
from app.application.relevance_filter import RelevanceFilter
from app.application.query_processor import QueryProcessor
from app.application.context_builder import ContextBuilder
from app.application.prompt_builder import PromptBuilder
from app.application.source_builder import SourceBuilder


def create_chat_model():
    if settings.CHAT_PROVIDER == "openai":
        return OpenAIChatModel()

    raise ValueError(
        f"Unsupported chat provider: {settings.CHAT_PROVIDER}"
    )


def create_embedding_model():
    if settings.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddingModel()

    raise ValueError(
        f"Unsupported embedding provider: "
        f"{settings.EMBEDDING_PROVIDER}"
    )


def create_notes_repository():
    if settings.VECTOR_STORE_PROVIDER == "chroma":
        return ChromaNotesRepository()

    raise ValueError(
        f"Unsupported vector store provider: "
        f"{settings.VECTOR_STORE_PROVIDER}"
    )


def create_rag_service() -> RAGService:
    return RAGService(
        chat_model=create_chat_model(),
        embedding_model=create_embedding_model(),
        notes_repository=create_notes_repository(),
        relevance_filter=RelevanceFilter(max_distance=None),
        query_processor=QueryProcessor(),
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        source_builder=SourceBuilder(),
    )