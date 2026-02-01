from typing import Any, Any, Optional

from app.application.dto.catalog_dtos import CatalogItemDTO, CatalogListDTO
from app.application.ports.catalog_repository import CatalogRepository

class ListCatalogItems:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self, 
                category: Optional[str] = None, 
                subcategory: Optional[str] = None,
                unit: Optional[str] = None,
                provider: Optional[str] = None,
                include_inactive: Optional[bool] = False
    ) -> CatalogListDTO:
        
        items: list[dict[str, Any]] = self.catalog_repository.get()

        filters = self._filters_builder(
            category=category,
            subcategory=subcategory,
            unit=unit,
            provider=provider
        )
        
        result: list[CatalogItemDTO] = []
        
        for item in items:
            if not include_inactive and not item.get("active", True):
                continue

            # Apply filters
            if filters:
                match = all(
                    item.get(k) == v for k, v in filters.items())
                if not match:
                    continue

            result.append(
                CatalogItemDTO(
                    item_id=item.get("item_id", ""),
                    name=item.get("name", ""),
                    category=item.get("category"),
                    subcategory=item.get("subcategory"),
                    description=item.get("description"),
                    unit=item.get("unit"),
                    provider=item.get("provider"),
                    active=item.get("active", True),
                    attributes=item.get("attributes", {}),
                    )
            )

        return CatalogListDTO(items=result)


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