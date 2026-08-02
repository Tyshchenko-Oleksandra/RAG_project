from streamlit import context

from app.domain.interfaces.chat_model import ChatModel
from app.domain.interfaces.embedding_model import EmbeddingModel
from app.domain.interfaces.notes_repository import NotesRepository
from app.domain.models import RetrievedChunk
from app.application.relevance_filter import RelevanceFilter
from app.application.query_processor import QueryProcessor
from app.application.context_builder import ContextBuilder
from app.application.prompt_builder import PromptBuilder
from app.application.source_builder import SourceBuilder


class RAGService:
    """Координує пошук у конспектах і генерацію відповіді."""
    def __init__(
    self,
    chat_model: ChatModel,
    embedding_model: EmbeddingModel,
    notes_repository: NotesRepository,
    relevance_filter: RelevanceFilter,
    query_processor: QueryProcessor,
    context_builder: ContextBuilder,
    prompt_builder: PromptBuilder,
    source_builder: SourceBuilder,
) -> None:
        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.notes_repository = notes_repository
        self.relevance_filter = relevance_filter
        self.query_processor = query_processor
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.source_builder = source_builder

    def answer_question(
        self,
        question: str,
        subject: str,
        limit: int = 8,
    ) -> dict:
        processed_question = self.query_processor.process(question)
        question_embedding = self.embedding_model.embed(processed_question) 

        chunks = self.notes_repository.search(
            embedding=question_embedding,
            subject=subject,
            limit=limit,
        )
        chunks = self.relevance_filter.filter(chunks)

        if not chunks:
            return {
                "answer": (
                    "У завантажених конспектах "
                    "я не знайшла цієї інформації."
                ),
                "sources": [],
            }

        context = self.context_builder.build(chunks)
        prompt = self.prompt_builder.build(
        question=processed_question,
        subject=subject,
        context=context,
)

        answer = self.chat_model.generate(prompt)
        sources = self.source_builder.build(chunks)

        return {
            "answer": answer,
            "sources": sources,
        }
    def get_subjects(self) -> list[str]:
        return self.notes_repository.get_subjects()
