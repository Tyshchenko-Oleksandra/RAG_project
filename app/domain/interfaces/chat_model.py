from typing import Protocol


class ChatModel(Protocol):
    """Контракт для моделей, які генерують текстову відповідь."""

    def generate(self, prompt: str) -> str:
        """Згенерувати відповідь на основі prompt."""
        ...