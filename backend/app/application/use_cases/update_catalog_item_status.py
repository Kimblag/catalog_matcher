from typing import Any
from app.application.ports.catalog_repository import CatalogRepository


class UpdateCatalogItemStatus:
    
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository


    def execute(self, item_id: str, active: bool) -> None:
        catalog: list[dict[str, Any]] = self.catalog_repository.get()
    
        for item in catalog:
            if item.get("item_id") == item_id:
                item["active"] = active
                break
        self.catalog_repository.save(catalog)
