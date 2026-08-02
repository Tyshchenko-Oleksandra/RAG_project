from openai import OpenAI

from app.core.config import settings


class OpenAIChatModel:
    """Реалізація ChatModel через OpenAI API."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.CHAT_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ти допомагаєш студенту шукати інформацію "
                        "в університетських конспектах."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            return "Модель не повернула відповідь."

        return content