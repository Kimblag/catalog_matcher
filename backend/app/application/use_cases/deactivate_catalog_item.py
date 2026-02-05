from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class DeactivateCatalogItem:
    
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository


    def execute(self, item_id: str) -> None:
        catalog: Catalog = self.catalog_repository.get()
        catalog.deactivate_item(item_id)
        self.catalog_repository.save(catalog)
