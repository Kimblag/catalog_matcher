import pytest
from unittest.mock import Mock

from app.application.use_cases.match_requirements import MatchRequirements
from app.application.exceptions.empty_requirement_file_exception import EmptyRequirementFileException
from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource


# Happy path
def test_execute_when_single_requirement_and_matches_exist_should_return_enriched_matches():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    raw_requirements = [{"Name": "Laptop", "Quantity": "1", "Unit": "unit"}]
    normalized_requirements = [{
        "name": "laptop",
        "quantity": "1",
        "unit": "unit",
        "description": "work laptop"
    }]

    file_reader.read_requirements.return_value = raw_requirements
    normalizer.normalize_requirements.return_value = normalized_requirements

    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(
        item_id="item-1",
        name="Laptop Dell",
        category="electronics",
        description="business laptop",
        unit="unit",
        provider="dell",
        attributes={"ram": "16gb"}
    )

    catalog_repository.get.return_value = catalog
    embedding_service.get_embedding.return_value = [0.1, 0.2, 0.3]
    vector_repository.search.return_value = [("item-1", 0.95)]

    use_case = MatchRequirements(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        embedding_service=embedding_service,
        vector_repository=vector_repository,
        top_k=3
    )

    # Act
    result = use_case.execute("requirements.csv")

    # Assert
    assert len(result) == 1

    entry = result[0]
    assert entry["requirement"] == normalized_requirements[0]
    assert len(entry["matches"]) == 1

    match = entry["matches"][0]
    assert match["catalog_item_id"] == "item-1"
    assert match["name"] == "Laptop Dell"
    assert match["category"] == "electronics"
    assert match["score"] == 0.95


def test_execute_when_multiple_requirements_should_return_matches_per_requirement():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}, {}]
    normalizer.normalize_requirements.return_value = [
        {"name": "item1", "quantity": "1", "unit": "u"},
        {"name": "item2", "quantity": "2", "unit": "u"},
    ]

    catalog_repository.get.return_value = Catalog(CatalogSource.MANUAL)
    embedding_service.get_embedding.return_value = [0.1]
    vector_repository.search.return_value = []

    use_case = MatchRequirements(
        file_reader,
        normalizer,
        catalog_repository,
        embedding_service,
        vector_repository
    )

    # Act
    result = use_case.execute("file.csv")

    # Assert
    assert len(result) == 2


def test_execute_should_call_embedding_service_with_composed_text():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize_requirements.return_value = [{
        "name": "hammer",
        "quantity": "2",
        "unit": "pcs",
        "attributes": {"material": "steel"}
    }]

    catalog_repository.get.return_value = Catalog(CatalogSource.MANUAL)
    embedding_service.get_embedding.return_value = [0.1]
    vector_repository.search.return_value = []

    use_case = MatchRequirements(
        file_reader,
        normalizer,
        catalog_repository,
        embedding_service,
        vector_repository
    )

    # Act
    use_case.execute("file.csv")

    # Assert
    embedding_service.get_embedding.assert_called_once()
    called_text = embedding_service.get_embedding.call_args[0][0]
    assert "name: hammer" in called_text
    assert "attributes:" in called_text


# Error path
def test_execute_when_requirement_file_is_empty_should_raise_exception():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = []

    use_case = MatchRequirements(
        file_reader,
        normalizer,
        catalog_repository,
        embedding_service,
        vector_repository
    )

    # Act & Assert
    with pytest.raises(EmptyRequirementFileException):
        use_case.execute("empty.csv")


def test_execute_when_vector_repository_returns_empty_should_return_empty_matches():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize_requirements.return_value = [{
        "name": "chair",
        "quantity": "1",
        "unit": "unit"
    }]

    catalog_repository.get.return_value = Catalog(CatalogSource.MANUAL)
    embedding_service.get_embedding.return_value = [0.1]
    vector_repository.search.return_value = []

    use_case = MatchRequirements(
        file_reader,
        normalizer,
        catalog_repository,
        embedding_service,
        vector_repository
    )

    # Act
    result = use_case.execute("file.csv")

    # Assert
    assert result[0]["matches"] == []


def test_execute_should_call_vector_repository_with_embedding_and_top_k():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize_requirements.return_value = [{
        "name": "monitor",
        "quantity": "1",
        "unit": "unit"
    }]

    catalog_repository.get.return_value = Catalog(CatalogSource.MANUAL)

    fake_embedding = [0.9, 0.8, 0.7]
    embedding_service.get_embedding.return_value = fake_embedding
    vector_repository.search.return_value = []

    use_case = MatchRequirements(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        embedding_service=embedding_service,
        vector_repository=vector_repository,
        top_k=5
    )

    # Act
    use_case.execute("requirements.csv")

    # Assert
    vector_repository.search.assert_called_once_with(
        query_embedding=fake_embedding,
        top_k=5
    )
