from typing import Any, Any, Optional

from app.application.dto.catalog_dtos import CatalogItemDTO, CatalogListDTO
from app.application.ports.catalog_repository import CatalogRepository


class ListCatalogItems:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self, include_inactive: Optional[bool] = False) -> CatalogListDTO:

        items: list[dict[str, Any]] = self.catalog_repository.get()

        result: list[CatalogItemDTO] = []

        for item in items:
            if not include_inactive and not item.get("active", True):
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
