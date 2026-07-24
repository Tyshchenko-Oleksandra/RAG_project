import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="university_notes")


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

    sources = [
        {
            "source": meta["source"],
            "chunk_index": meta["chunk_index"]
        }
        for meta in metadatas
    ]

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