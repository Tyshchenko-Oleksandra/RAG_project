import chromadb

from app.core.config import settings
from app.domain.models import RetrievedChunk


class ChromaNotesRepository:
    """Реалізація NotesRepository через ChromaDB."""

    def __init__(self) -> None:
        client = chromadb.PersistentClient(path=settings.CHROMA_DIR)

        self.collection = client.get_or_create_collection(
            name=settings.COLLECTION_NAME
        )

    def search(
        self,
        embedding: list[float],
        subject: str,
        limit: int = 8,
    ) -> list[RetrievedChunk]:
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=limit,
            where={"subject": subject},
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            chunks.append(
                RetrievedChunk(
                    text=document,
                    metadata=metadata or {},
                    distance=distance,
                )
            )

        return chunks

    def get_subjects(self) -> list[str]:
        results = self.collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])

        subjects = sorted(
            {
                metadata["subject"]
                for metadata in metadatas
                if metadata and "subject" in metadata
            }
        )

        return subjects