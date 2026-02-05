from app.application.exceptions.unsupported_catalog_source_exception import UnsupportedCatalogSourceException
from app.domain.enums.catalog_sources import CatalogSource


def resolve_source(file_path: str) -> CatalogSource:
        extension = file_path.rsplit(".", 1)[-1].lower()

        if extension == "csv":
            return CatalogSource.CSV
        if extension == "xlsx":
            return CatalogSource.XLSX

        raise UnsupportedCatalogSourceException(extension) 