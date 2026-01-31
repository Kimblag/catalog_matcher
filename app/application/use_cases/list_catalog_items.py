from typing import Optional

from app.application.dto.catalog_list_dto import CatalogItemDTO, CatalogListDTO
from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class ListCatalogItems:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self, 
                filters: Optional[dict[str, str]] = None, 
                include_inactive: bool = False) -> CatalogListDTO:
        catalog: Catalog = self.catalog_repository.get()
        items = catalog.get_items()

        filtered_items = []

        for item in items.values():
            if not include_inactive and not item.active:
                continue

            # Apply filters
            if filters:
                match = all(
                    getattr(item, k, None) == v for k, v in filters.items())

                if not match:
                    continue

            dto = CatalogItemDTO(
                item_id=item.item_id,
                name=item.name,
                category=item.category,
                description=item.description,
                subcategory=item.subcategory,
                unit=item.unit,
                provider=item.provider,
                active=item.active,
                attributes=item.attributes,
            )
            filtered_items.append(dto)


        return CatalogListDTO(catalog=filtered_items)
