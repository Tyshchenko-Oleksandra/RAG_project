import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    CHROMA_DIR: str = os.getenv(
        "CHROMA_DIR",
        "storage/chroma_db",
    )
    COLLECTION_NAME: str = os.getenv(
        "COLLECTION_NAME",
        "university_notes",
    )

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "text-embedding-3-small",
    )
    CHAT_MODEL: str = os.getenv(
        "CHAT_MODEL",
        "gpt-4o-mini",
    )

    CHAT_PROVIDER: str = os.getenv(
        "CHAT_PROVIDER",
        "openai",
    )
    EMBEDDING_PROVIDER: str = os.getenv(
        "EMBEDDING_PROVIDER",
        "openai",
    )
    VECTOR_STORE_PROVIDER: str = os.getenv(
        "VECTOR_STORE_PROVIDER",
        "chroma",
    )
settings = Settings()