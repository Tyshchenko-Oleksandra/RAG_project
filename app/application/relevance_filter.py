from app.domain.models import RetrievedChunk


class RelevanceFilter:
    """Відкидає chunks, які недостатньо близькі до запитання."""

    def __init__(self, max_distance: float | None = None) -> None:
        self.max_distance = max_distance

    def filter(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        if self.max_distance is None:
            return chunks

        return [
            chunk
            for chunk in chunks
            if (
                chunk.distance is not None
                and chunk.distance <= self.max_distance
            )
        ]