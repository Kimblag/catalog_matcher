from typing import Any
from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class DeactivateCatalogItem:
    
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository


    def execute(self, item_id: str) -> None:
        catalog: list[dict[str, Any]] = self.catalog_repository.get()
    
        for item in catalog:
            if item.get("id") == item_id:
                item["active"] = False
                break
        self.catalog_repository.save(catalog)
