from openai import OpenAI

from app.core.config import settings


class OpenAIEmbeddingModel:
    """Реалізація EmbeddingModel через OpenAI API."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding