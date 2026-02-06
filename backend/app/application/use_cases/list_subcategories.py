from typing import Any

from app.application.dto.catalog_dtos import SubcategoriesListDTO
from app.application.ports.catalog_repository import CatalogRepository


class ListSubcategories:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self) -> SubcategoriesListDTO:

        items: list[dict[str, Any]] = self.catalog_repository.get()

        subcategories_set: set[str] = {
            (str(item.get("subcategory"))) for item in items if item.get("subcategory")
        }

        return SubcategoriesListDTO(subcategories=list(subcategories_set))
