from typing import Any, Protocol

class CatalogRepository(Protocol):
    def get(self) -> list[dict[str, Any]]:
        ...
    
    def save(self, catalog: list[dict[str, Any]]) -> None:
        ...