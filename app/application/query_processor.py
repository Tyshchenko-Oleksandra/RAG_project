class QueryProcessor:
    """Готує запит користувача перед створенням embedding."""

    def process(self, question: str) -> str:
        normalized_question = " ".join(question.split())

        if not normalized_question:
            raise ValueError("Питання не може бути порожнім.")

        return normalized_question