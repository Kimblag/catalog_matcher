import pytest
from unittest.mock import Mock, call

from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.exceptions.empty_catalog_file_exception import EmptyCatalogFileException
from app.application.exceptions.unsupported_catalog_source_exception import UnsupportedCatalogSourceException
from app.application.use_cases.load_catalog import LoadCatalog
from app.domain.entities.catalog import Catalog


# Happy path
def test_load_catalog_happy_path():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    raw_items = [{"item_id": "1"}]
    normalized_items = [{"item_id": "1"}]

    file_reader.read_catalog.return_value = raw_items
    normalizer.normalize_catalog_items.return_value = normalized_items

    use_case = LoadCatalog(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=repository,
    )

    # Act
    result = use_case.execute("catalog.csv")

    # Assert
    repository.save.assert_called_once()
    assert result is None


# Error path
def test_load_catalog_empty_file():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = []

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act & Assert
    with pytest.raises(EmptyCatalogFileException):
        use_case.execute("catalog.csv")


def test_load_catalog_normalizer_fails():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.side_effect = CatalogNormalizationException("error")

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act & Assert
    with pytest.raises(CatalogNormalizationException):
        use_case.execute("catalog.csv")

def test_load_catalog_unsupported_source():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.return_value = [{"item_id": "1"}]

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act & Assert
    with pytest.raises(UnsupportedCatalogSourceException):
        use_case.execute("catalog.txt")


def test_load_catalog_batches_items(monkeypatch):
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    items = [{"item_id": str(i)} for i in range(120)]
    file_reader.read_catalog.return_value = items
    normalizer.normalize_catalog_items.return_value = items

    add_batch_mock = Mock()
    monkeypatch.setattr(Catalog, "add_or_update_items_batch", add_batch_mock)

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act
    use_case.execute("catalog.csv")

    # Assert
    assert add_batch_mock.call_count == 3 


def test_load_catalog_calls_reader_once():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.return_value = [{"item_id": "1"}]

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act
    use_case.execute("catalog.csv")

    # Assert
    file_reader.read_catalog.assert_called_once_with("catalog.csv")


def test_load_catalog_calls_normalizer_once():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.return_value = [{"item_id": "1"}]

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act
    use_case.execute("catalog.csv")

    # Assert
    normalizer.normalize_catalog_items.assert_called_once()


def test_load_catalog_persists_once():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.return_value = [{"item_id": "1"}]

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act
    use_case.execute("catalog.csv")

    # Assert
    repository.save.assert_called_once()


def test_load_catalog_does_not_return_value():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    repository = Mock()

    file_reader.read_catalog.return_value = [{"item_id": "1"}]
    normalizer.normalize_catalog_items.return_value = [{"item_id": "1"}]

    use_case = LoadCatalog(file_reader, normalizer, repository)

    # Act
    result = use_case.execute("catalog.csv")

    # Assert
    assert result is None
