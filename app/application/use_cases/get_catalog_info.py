from datetime import datetime
from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class GetCatalogInfo:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    
    def execute(self) -> tuple[datetime, str, int]:
        catalog: Catalog = self.catalog_repository.get()
        
        metadata: tuple[datetime, str, int] = (
            catalog.get_last_updated(),
            catalog.get_source(), 
            catalog.get_version())

        return metadata