import pytest
from unittest.mock import Mock, patch

from app.application.use_cases.match_requirements import MatchRequirements
from app.application.exceptions.empty_requirement_file_exception import EmptyRequirementFileException


def test_execute_single_requirement_with_matches():
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
    normalizer.normalize.return_value = normalized_requirements

    catalog_repository.get.return_value = [{
        "item_id": "item-1",
        "name": "Laptop Dell",
        "category": "electronics",
        "description": "business laptop",
        "unit": "unit",
        "provider": "dell",
        "active": True,
        "attributes": {"ram": "16gb"}
    }]

    embedding_service.get_embedding.return_value = [0.1, 0.2, 0.3]
    vector_repository.search.return_value = [("item-1", 0.05)]

    with patch('app.application.use_cases.match_requirements.settings') as mock_settings:
        mock_settings.MAX_DISTANCE = 0.5

        use_case = MatchRequirements(
            file_reader=file_reader,
            normalizer=normalizer,
            catalog_repository=catalog_repository,
            embedding_service=embedding_service,
            vector_repository=vector_repository,
            top_k=3
        )

        # Act
        result = use_case.execute(b"file content")

    # Assert
    assert len(result.results) == 1

    entry = result.results[0]
    assert entry.requirement == normalized_requirements[0]
    assert len(entry.matches) == 1

    match = entry.matches[0]
    assert match.catalog_item_id == "item-1"
    assert match.name == "Laptop Dell"
    assert match.category == "electronics"
    assert match.score == 0.05


def test_execute_multiple_requirements():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}, {}]
    normalizer.normalize.return_value = [
        {"name": "item1", "quantity": "1", "unit": "u"},
        {"name": "item2", "quantity": "2", "unit": "u"},
    ]

    catalog_repository.get.return_value = []
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
    result = use_case.execute(b"content")

    # Assert
    assert len(result.results) == 2


def test_execute_calls_embedding_with_composed_text():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize.return_value = [{
        "name": "hammer",
        "quantity": "2",
        "unit": "pcs",
        "attributes": {"material": "steel"}
    }]

    catalog_repository.get.return_value = []
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
    use_case.execute(b"content")

    # Assert
    embedding_service.get_embedding.assert_called_once()
    called_text = embedding_service.get_embedding.call_args[0][0]
    assert "name: hammer" in called_text
    assert "attributes: material:steel" in called_text


def test_execute_empty_file_raises_exception():
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
        use_case.execute(b"empty")


def test_execute_no_vector_matches_returns_empty():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize.return_value = [{
        "name": "chair",
        "quantity": "1",
        "unit": "unit"
    }]

    catalog_repository.get.return_value = []
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
    result = use_case.execute(b"content")

    # Assert
    assert result.results[0].matches == []


def test_execute_calls_vector_repository_with_embedding_and_top_k():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize.return_value = [{
        "name": "monitor",
        "quantity": "1",
        "unit": "unit"
    }]

    catalog_repository.get.return_value = []

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
    use_case.execute(b"content")

    # Assert
    vector_repository.search.assert_called_once_with(
        query_embedding=fake_embedding,
        top_k=5
    )


def test_execute_filters_by_max_distance():
    # Arrange
    file_reader = Mock()
    normalizer = Mock()
    catalog_repository = Mock()
    embedding_service = Mock()
    vector_repository = Mock()

    file_reader.read_requirements.return_value = [{}]
    normalizer.normalize.return_value = [{"name": "item", "unit": "u"}]

    catalog_repository.get.return_value = [
        {
            "item_id": "1",
            "name": "a",
            "category": "c",
            "description": "desc1",
            "active": True
        },
        {
            "item_id": "2",
            "name": "b",
            "category": "c",
            "description": "desc2",
            "active": True
        }
    ]

    embedding_service.get_embedding.return_value = [0.1]
    vector_repository.search.return_value = [("1", 0.05), ("2", 0.9)]

    with patch('app.application.use_cases.match_requirements.settings') as mock_settings:
        mock_settings.MAX_DISTANCE = 0.5

        use_case = MatchRequirements(
            file_reader, normalizer, catalog_repository,
            embedding_service, vector_repository
        )

        # Act
        result = use_case.execute(b"content")

    # Assert
    assert len(result.results[0].matches) == 1
    assert result.results[0].matches[0].catalog_item_id == "1"