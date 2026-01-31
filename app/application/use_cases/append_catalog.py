from itertools import batched

from app.application.constants import BATCH_SIZE
from app.application.exceptions.empty_catalog_file_exception import \
    EmptyCatalogFileException
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.embedding_service import EmbeddingService
from app.application.ports.file_reader import FileReader
from app.application.ports.normalizer import NormalizerCatalog
from app.application.ports.vector_repository import VectorRepository
from app.application.utils.catalog_helpers import resolve_source
from app.domain.entities.catalog import Catalog


class AppendCatalog:

    def __init__(self,
                 file_reader: FileReader,
                 normalizer: NormalizerCatalog,
                 catalog_repository: CatalogRepository,
                 vector_repository: VectorRepository,
                 embedding_service: EmbeddingService):
        self.file_reader = file_reader
        self.normalizer = normalizer
        self.catalog_repository = catalog_repository
        self.vector_repository = vector_repository
        self.embedding_service = embedding_service

    
    def execute(self, file_path: str) -> None:
        # Map enum
        source = resolve_source(file_path)

        # Open and read the file
        raw_items = self.file_reader.read_catalog(file_path)
        
        if len(raw_items) == 0:
            raise EmptyCatalogFileException("Catalog does not contains any item.")

        # normalize items. Let the normalizer exception raise
        normalized_items = self.normalizer.normalize_catalog_items(raw_items)


        # save to the Catalog
        catalog: Catalog = Catalog(source)

        # Add items to the catalog by batches using itertools
        for batch in batched(normalized_items, BATCH_SIZE):
            catalog.add_or_update_items_batch(list(batch))

        # Persist the catalog.
        self.catalog_repository.save(catalog)

        # Create embeddings
        vector_items = []
        for item in catalog.get_items().values():
            # Generate text for openai
            text_to_embed = (
                f"name: {item.name} | "
                f"category: {item.category} | "
                f"subcategory: {item.subcategory or ''} | "
                f"description: {item.description} | "
                f"unit: {item.unit or ''} | "
                f"provider: {item.provider or ''} | "
                f"attributes: {','.join(f'{k}:{v}' for k,v in item.attributes.items())} | "
                f"active: {item.active}"
            )
            embedding = self.embedding_service.get_embedding(text_to_embed)
            vector_items.append({
                "item_id": item.item_id,
                "embedding": embedding
            })

        # save embeddings
        self.vector_repository.save(vector_items)
