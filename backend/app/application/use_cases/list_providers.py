from typing import Any

from app.application.dto.catalog_dtos import ProvidersListDTO
from app.application.ports.catalog_repository import CatalogRepository


class ListProviders:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def execute(self) -> ProvidersListDTO:

        items: list[dict[str, Any]] = self.catalog_repository.get()

        providers_set: set[str] = {
            (str(item.get("provider"))) for item in items if item.get("provider")
        }

        return ProvidersListDTO(providers=list(providers_set))
