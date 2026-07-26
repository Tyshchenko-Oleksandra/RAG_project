import chromadb

from app.core.config import settings


chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name=settings.COLLECTION_NAME)


def get_collection():
    return collection


def get_available_subjects() -> list[str]:
    results = collection.get(include=["metadatas"])
    metadatas = results.get("metadatas", [])

    subjects = sorted({
        meta["subject"]
        for meta in metadatas
        if meta and "subject" in meta
    })

    return subjects