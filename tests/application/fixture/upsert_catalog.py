from unittest.mock import Mock
import pytest

from app.application.use_cases.upsert_catalog import UpsertCatalog

@pytest.fixture
def file_reader():
    return Mock()

@pytest.fixture
def normalizer():
    return Mock()

@pytest.fixture
def catalog_repository():
    return Mock()

@pytest.fixture
def vector_repository():
    return Mock()

@pytest.fixture
def embedding_service():
    return Mock()

@pytest.fixture
def use_case(
    file_reader,
    normalizer,
    catalog_repository,
    vector_repository,
    embedding_service,
):
    return UpsertCatalog(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )
