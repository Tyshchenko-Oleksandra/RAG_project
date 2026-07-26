import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="university_notes")

def get_available_subjects() -> list[str]:
    results = collection.get(include=["metadatas"])

    metadatas = results.get("metadatas", [])

    subjects = sorted({
        meta["subject"]
        for meta in metadatas
        if meta and "subject" in meta
    })

    return subjects


def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ти допомагаєш студенту шукати інформацію в університетських конспектах."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

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

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }
if __name__ == "__main__":
    subject = input("Введи предмет, наприклад chemistry/math/physics: ")
    question = input("Введи питання: ")

    result = answer_question(question, subject)

    print("\nВідповідь:")
    print(result["answer"])

    print("\nДжерела:")
    for source in result["sources"]:
        print(source)