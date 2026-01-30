from itertools import batched

from app.application.exceptions.empty_catalog_file_exception import \
    EmptyCatalogFileException
from app.application.exceptions.unsupported_catalog_source_exception import \
    UnsupportedCatalogSourceException
from app.application.ports import file_reader
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.file_reader import FileReader
from app.application.ports.normalizer import NormalizerCatalog
from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource


class LoadCatalog:

    _BATCH_SIZE: int = 50

    def __init__(self,
                 file_reader: FileReader,
                 normalizer: NormalizerCatalog,
                 catalog_repository: CatalogRepository):
        self.file_reader = file_reader
        self.normalizer = normalizer
        self.catalog_repository = catalog_repository

    
    def execute(self, file_path: str) -> None:
        
        # Map enum
        source = self._resolve_source(file_path)

        # Open and read the file
        raw_items = self.file_reader.read_catalog(file_path)
        
        if len(raw_items) == 0:
            raise EmptyCatalogFileException("Catalog does not contains any item.")

        # normalize items. Let the normalizer exception raise
        normalized_items = self.normalizer.normalize_catalog_items(raw_items)


        # save to the Catalog
        catalog = Catalog(source)

        # Add items to the catalog by batches using itertools
        for batch in batched(normalized_items, self._BATCH_SIZE):
            catalog.add_or_update_items_batch(list(batch))

        # Persist the catalog.
        self.catalog_repository.save(catalog)
    

    def _resolve_source(self, file_path: str) -> CatalogSource:
        extension = file_path.rsplit(".", 1)[-1].lower()

        if extension == "csv":
            return CatalogSource.CSV
        if extension == "xlsx":
            return CatalogSource.XLSX

        raise UnsupportedCatalogSourceException(extension)