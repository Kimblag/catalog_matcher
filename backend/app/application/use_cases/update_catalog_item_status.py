from typing import Any
from app.application.ports.catalog_repository import CatalogRepository
from app.application.utils.catalog_helpers import convert_to_catalog_items
from app.domain.entities.catalog_item import CatalogItem
from app.domain.entities.catalog import Catalog


class UpdateCatalogItemStatus:

    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self, item_id: str, active: bool) -> None:
        persisted_items: list[dict[str, Any]] = self.catalog_repository.get()
        catalog_items: list[CatalogItem] = convert_to_catalog_items(
            items_data=persisted_items
        )
        catalog = Catalog()
        catalog.batch_upsert(catalog_items)
        catalog.update_item_status(item_id=item_id, active=active)
      
        self.catalog_repository.save(catalog=[
            {
                "item_id": item.item_id,
                "name": item.name,
                "category": item.category,
                "subcategory": item.subcategory,
                "description": item.description,
                "unit": item.unit,
                "provider": item.provider,
                "attributes": item.attributes,
                "active": item.active,
            }
            for item in catalog.get_items().values()
        ])
