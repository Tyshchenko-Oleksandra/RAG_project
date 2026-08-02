from typing import Protocol

from app.domain.models import RetrievedChunk


class NotesRepository(Protocol):
    """Контракт для пошуку та збереження фрагментів конспектів."""

    def search(
        self,
        embedding: list[float],
        subject: str,
        limit: int = 8,
    ) -> list[RetrievedChunk]:
        """Знайти релевантні фрагменти конспектів."""
        ...

    def get_subjects(self) -> list[str]:
        """Повернути список доступних предметів."""
        ...