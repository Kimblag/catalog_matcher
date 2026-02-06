from typing import Any

from app.application.dto.catalog_dtos import CategoriesListDTO
from app.application.ports.catalog_repository import CatalogRepository


class ListCategories:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self) -> CategoriesListDTO:

        items: list[dict[str, Any]] = self.catalog_repository.get()

        categories_set: set[str] = {
            (str(item.get("category"))) for item in items if item.get("category")
        }

        return CategoriesListDTO(categories=list(categories_set))
