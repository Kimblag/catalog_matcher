from itertools import batched
from typing import Any

from app.application.constants import BATCH_SIZE
from app.application.exceptions.empty_catalog_file_exception import \
    EmptyCatalogFileException
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.embedding_service import EmbeddingService
from app.application.ports.file_reader import FileReader
from app.application.ports.normalizer import Normalizer
from app.application.ports.vector_repository import VectorRepository
from app.domain.entities.catalog import Catalog
from app.domain.entities.catalog_item import CatalogItem


class UpsertCatalog:

    def __init__(self,
                 file_reader: FileReader,
                 normalizer: Normalizer,
                 catalog_repository: CatalogRepository,
                 vector_repository: VectorRepository,
                 embedding_service: EmbeddingService):
        self.file_reader = file_reader
        self.normalizer = normalizer
        self.catalog_repository = catalog_repository
        self.vector_repository = vector_repository
        self.embedding_service = embedding_service

    
    def execute(self, file_bytes: bytes) -> None:
        # Open and read the file
        raw_items = self.file_reader.read_catalog(file_bytes)
        
        if len(raw_items) == 0:
            raise EmptyCatalogFileException("Catalog does not contains any item.")

        # normalize items. Let the normalizer exception raise
        normalized_items = self.normalizer.normalize(raw_items)

        # Get the persisted items & Add items to the catalog by batches using itertools
        catalog: Catalog = self._build_catalog_from_persistence()
        self._apply_new_items(catalog, normalized_items)
        
        # Persist the catalog.
        items_to_save = self._map_catalog_to_persistence(catalog)
        self.catalog_repository.save(items_to_save)

        # Create embeddings & save embeddings
        self._recreate_embeddings(catalog)


    def _build_catalog_from_persistence(self) -> Catalog:
        catalog = Catalog()

        persisted_items: list[dict[str, Any]] = self.catalog_repository.get() or []

        for batch in batched(persisted_items, BATCH_SIZE):
            catalog.batch_upsert(list(batch))

        return catalog

    

    def _apply_new_items(
            self, 
            catalog: Catalog, 
            normalized_items: list[dict[str, Any]]) -> None:
        
        for batch in batched(normalized_items, BATCH_SIZE):
            catalog.batch_upsert(list(batch))


    def _map_catalog_to_persistence(self, catalog: Catalog):
        return [
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
        ]
    

    def _recreate_embeddings(self, catalog: Catalog) -> None:
        vector_items = []

        for item in catalog.get_items().values():
            text = self._build_embedding_text(item)
            embedding = self.embedding_service.get_embedding(text)
            vector_items.append({
                "item_id": item.item_id,
                "embedding": embedding
            })

        self.vector_repository.save(vector_items)


    def _build_embedding_text(self, item: CatalogItem) -> str:
        return (
            f"name: {item.name} | "
            f"category: {item.category} | "
            f"subcategory: {item.subcategory or ''} | "
            f"description: {item.description} | "
            f"unit: {item.unit or ''} | "
            f"provider: {item.provider or ''} | "
            f"attributes: {','.join(f'{k}:{v}' for k,v in item.attributes.items())} | "
            f"active: {item.active}"
        )
