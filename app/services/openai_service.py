from openai import OpenAI

from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.CHAT_MODEL,
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

    return response.choices[0].message.content