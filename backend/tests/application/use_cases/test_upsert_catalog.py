from unittest.mock import Mock
import pytest

from app.application.use_cases.upsert_catalog import UpsertCatalog
from app.application.exceptions.empty_catalog_file_exception import EmptyCatalogFileException
from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.constants import BATCH_SIZE


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


def test_execute_valid_catalog_should_append_and_persist(
    use_case,
    file_reader,
    normalizer,
    catalog_repository,
    vector_repository,
    embedding_service,
):
    # Arrange
    raw_items = [
        {
            "Item_Id": "A1",
            "Name": "Laptop",
            "Category": "Hardware",
            "Description": "Portable computer",
        }
    ]

    normalized_items = [
        {
            "item_id": "a1",
            "name": "laptop",
            "category": "hardware",
            "description": "portable computer",
            "active": True,
        }
    ]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize.return_value = normalized_items
    catalog_repository.get.return_value = []
    embedding_service.get_embedding.return_value = [0.1, 0.2, 0.3]

    # Act
    use_case.execute(b"file content")

    # Assert — lectura y normalización
    file_reader.read_catalog.assert_called_once_with(b"file content")
    normalizer.normalize.assert_called_once_with(raw_items)

    # Assert — persistencia de catálogo
    catalog_repository.get.assert_called_once()
    catalog_repository.save.assert_called_once()

    saved_items = catalog_repository.save.call_args.args[0]
    assert len(saved_items) == 1
    assert saved_items[0]["item_id"] == "a1"

    # Assert — embeddings
    embedding_service.get_embedding.assert_called_once()
    vector_repository.save.assert_called_once()

    vector_items = vector_repository.save.call_args.args[0]
    assert vector_items[0]["item_id"] == "a1"
    assert vector_items[0]["embedding"] == [0.1, 0.2, 0.3]


def test_execute_empty_file_should_fail(
    use_case,
    file_reader,
):
    # Arrange
    file_reader.read_catalog.return_value = []

    # Act / Assert
    with pytest.raises(EmptyCatalogFileException):
        use_case.execute(b"content")

    file_reader.read_catalog.assert_called_once()


def test_execute_normalizer_fails_should_propagate(
    use_case,
    file_reader,
    normalizer,
):
    # Arrange
    raw_items = [
        {"item_id": "1", "name": "x", "category": "y", "description": "z"}
    ]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize.side_effect = CatalogNormalizationException(
        "invalid catalog"
    )

    # Act / Assert
    with pytest.raises(CatalogNormalizationException):
        use_case.execute(b"content")

    file_reader.read_catalog.assert_called_once()
    normalizer.normalize.assert_called_once_with(raw_items)


def test_execute_persisted_items_exist_should_merge(
    use_case,
    file_reader,
    normalizer,
    catalog_repository,
    embedding_service,
):
    # Arrange
    raw_items = [
        {
            "item_id": "new",
            "name": "new item",
            "category": "cat",
            "description": "desc",
        }
    ]

    normalized_items = [
        {
            "item_id": "new",
            "name": "new item",
            "category": "cat",
            "description": "desc",
            "active": True,
        }
    ]

    persisted_items = [
        {
            "item_id": "old",
            "name": "old item",
            "category": "cat",
            "description": "desc",
            "active": True,
        }
    ]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize.return_value = normalized_items
    catalog_repository.get.return_value = persisted_items
    embedding_service.get_embedding.return_value = [0.1]

    # Act
    use_case.execute(b"content")

    # Assert
    saved_items = catalog_repository.save.call_args.args[0]
    item_ids = {item["item_id"] for item in saved_items}

    assert item_ids == {"old", "new"}


def test_execute_items_exceed_batch_size_should_batch(
    use_case,
    file_reader,
    normalizer,
    catalog_repository,
    embedding_service,
):
    # Arrange
    raw_items = [
        {
            "item_id": f"id_{i}",
            "name": f"name_{i}",
            "category": "cat",
            "description": "desc",
        }
        for i in range(BATCH_SIZE + 1)
    ]

    normalized_items = [
        {
            "item_id": f"id_{i}",
            "name": f"name_{i}",
            "category": "cat",
            "description": "desc",
            "active": True,
        }
        for i in range(BATCH_SIZE + 1)
    ]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize.return_value = normalized_items
    catalog_repository.get.return_value = []
    embedding_service.get_embedding.return_value = [0.1]

    # Act
    use_case.execute(b"content")

    # Assert
    saved_items = catalog_repository.save.call_args.args[0]
    assert len(saved_items) == BATCH_SIZE + 1


def test_execute_should_generate_embeddings_for_all_items(
    use_case,
    file_reader,
    normalizer,
    catalog_repository,
    embedding_service,
    vector_repository,
):
    # Arrange
    raw_items = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
        }
    ]

    normalized_items = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
            "active": True,
        }
    ]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize.return_value = normalized_items
    catalog_repository.get.return_value = []
    embedding_service.get_embedding.return_value = [0.9]

    # Act
    use_case.execute(b"content")

    # Assert
    embedding_service.get_embedding.assert_called_once()
    vector_repository.save.assert_called_once()

    vectors = vector_repository.save.call_args.args[0]
    assert vectors == [{"item_id": "1", "embedding": [0.9]}]


def test_execute_should_not_return_any_value(
    use_case,
    file_reader,
    normalizer,
    catalog_repository,
    embedding_service,
):
    # Arrange
    file_reader.read_catalog.return_value = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
        }
    ]

    normalized_items = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
            "active": True,
        }
    ]

    normalizer.normalize.return_value = normalized_items
    catalog_repository.get.return_value = []
    embedding_service.get_embedding.return_value = [0.1]

    # Act
    result = use_case.execute(b"content")

    # Assert
    assert result is None