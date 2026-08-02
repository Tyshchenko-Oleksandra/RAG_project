from typing import Protocol


class EmbeddingModel(Protocol):
    """Контракт для моделей, які перетворюють текст на embedding-вектор."""

    def embed(self, text: str) -> list[float]:
        """Створити embedding для тексту."""
        ...