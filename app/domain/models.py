from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievedChunk:
    text: str
    metadata: dict[str, Any]
    distance: float | None = None