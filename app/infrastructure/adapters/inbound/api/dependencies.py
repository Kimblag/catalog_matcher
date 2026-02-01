# File dependencies
from pathlib import Path

from fastapi import Depends

from app.application.normalizers.catalog_normalizer import CatalogNormalizer
from app.application.normalizers.requirements_normalizer import RequirementNormalizer
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.embedding_service import EmbeddingService
from app.application.ports.vector_repository import VectorRepository
from app.infrastructure.adapters.outbound.catalog.catalog_repository_csv import (
    CatalogRepositoryCSV,
)
from app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai import (
    OpenAIEmbeddingService,
)
from app.infrastructure.adapters.outbound.files.file_reader_csv import FileReaderCSV
from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import (
    VectorRepositoryFAISS,
)
from app.infrastructure.config import settings


def get_file_reader() -> FileReaderCSV:
    return FileReaderCSV()


# Repository dependencies
def get_catalog_repository() -> CatalogRepository:
    return CatalogRepositoryCSV(csv_path=Path(settings.REPOSITORY_FILE_PATH))


# Service dependencies
def get_embedding_service() -> EmbeddingService:
    return OpenAIEmbeddingService()


def get_vector_repository() -> VectorRepository:
    return VectorRepositoryFAISS(
        dimension=settings.VECTOR_DIMENSION, path=Path(settings.VECTOR_FILE_PATH)
    )


# Normalizer dependency
def get_catalog_normalizer() -> CatalogNormalizer:
    return CatalogNormalizer()


def get_requirement_normalizer() -> RequirementNormalizer:
    return RequirementNormalizer()
