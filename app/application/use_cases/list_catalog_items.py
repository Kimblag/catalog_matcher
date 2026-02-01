from typing import Any, Any, Optional

from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class ListCatalogItems:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self, 
                category: Optional[str] = None, 
                subcategory: Optional[str] = None,
                unit: Optional[str] = None,
                provider: Optional[str] = None,
                include_inactive: Optional[bool] = False) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = self.catalog_repository.get()

        filtered_items = []
        filters = self._filters_builder(
            category=category,
            subcategory=subcategory,
            unit=unit,
            provider=provider
        )
        for item in items:
            if not include_inactive and not item.get("active", True):
                continue

            # Apply filters
            if filters:
                match = all(
                    item.get(k) == v for k, v in filters.items())
                if not match:
                    continue

            dto = {
                "item_id": item.get("item_id", ""),
                "name": item.get("name", ""),
                "category": item.get("category", ""),
                "description": item.get("description", ""),
                "subcategory": item.get("subcategory", ""),
                "unit": item.get("unit", ""),
                "provider": item.get("provider"),
                "active": item.get("active", True),
                "attributes": item.get("attributes", {}),
            }           
            filtered_items.append(dto)


        return filtered_items


    def _filters_builder(self, 
                         category: Optional[str],
                         subcategory: Optional[str],
                         unit: Optional[str],
                         provider: Optional[str]) -> dict[str, str]:
        filters = {}
        if category:
            filters["category"] = category
        if subcategory:
            filters["subcategory"] = subcategory
        if unit:
            filters["unit"] = unit
        if provider:
            filters["provider"] = provider
        return filters