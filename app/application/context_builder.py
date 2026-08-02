from app.domain.models import RetrievedChunk


class ContextBuilder:
    """Будує текстовий контекст із релевантних chunks."""

    def build(self, chunks: list[RetrievedChunk]) -> str:
        return "\n\n---\n\n".join(
            chunk.text.strip()
            for chunk in chunks
            if chunk.text.strip()
        )