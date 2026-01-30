from typing import Protocol

from app.domain.entities.catalog import Catalog


class CatalogRepository(Protocol):
    def get(self) -> Catalog:
        ...
    
    def save(self, catalog: Catalog) -> None:
        ...