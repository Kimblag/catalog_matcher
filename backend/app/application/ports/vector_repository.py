from typing import Protocol


class VectorRepository(Protocol):
    def save(self, items: list[dict]) -> None:
        ...

    def search(self, query_embedding: list[float], top_k: int) -> list[tuple[str, float]]:
        ...