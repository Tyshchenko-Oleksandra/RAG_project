from app.services.vector_store_service import get_collection
from app.services.openai_service import create_embedding, generate_answer

collection = get_collection()


def search_notes(question: str, subject: str, n_results: int = 8):
    question_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        where={"subject": subject}
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas


def build_sources(metadatas: list[dict]) -> list[dict]:
    sources = []

    for meta in metadatas:
        source_info = {
            "source": meta.get("source"),
            "subject": meta.get("subject"),
            "content_type": meta.get("content_type"),
            "chunk_index": meta.get("chunk_index")
        }

        if meta.get("page") is not None:
            source_info["page"] = meta.get("page")
            source_info["label"] = f'{meta.get("source")}, сторінка {meta.get("page")}'

        elif meta.get("slide") is not None:
            source_info["slide"] = meta.get("slide")
            source_info["label"] = f'{meta.get("source")}, слайд {meta.get("slide")}'

        else:
            source_info["label"] = f'{meta.get("source")}, chunk {meta.get("chunk_index")}'

        sources.append(source_info)

    return sources


def answer_question(question: str, subject: str) -> dict:
    documents, metadatas = search_notes(question, subject)

    if not documents:
        return {
            "answer": "Я не знайшла інформації по цьому питанню в конспектах.",
            "sources": []
        }

    context = "\n\n---\n\n".join(documents)

    prompt = f"""
Ти навчальний асистент. Відповідай тільки на основі контексту нижче.
Якщо відповіді в контексті немає, скажи: "У завантажених конспектах я не знайшла цієї інформації."
Не вигадуй.

Предмет: {subject}

Контекст:
{context}

Питання:
{question}
"""

    answer = generate_answer(prompt)
    sources = build_sources(metadatas)

    return {
        "answer": answer,
        "sources": sources
    }