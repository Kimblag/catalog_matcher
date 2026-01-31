from typing import Protocol


class EmbeddingService(Protocol):
    def get_embedding(self, text: str) -> list[float]:
        ...