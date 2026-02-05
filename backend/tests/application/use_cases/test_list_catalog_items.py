import pytest
from unittest.mock import Mock

from app.application.use_cases.list_catalog_items import ListCatalogItems


def test_list_catalog_items_happy_path():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {
            "item_id": "1",
            "name": "item1",
            "category": "cat1",
            "description": "desc1",
            "active": True,
        },
        {
            "item_id": "2",
            "name": "item2",
            "category": "cat2",
            "description": "desc2",
            "active": True,
        }
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result.items) == 2
    assert all(item.active for item in result.items)


def test_list_catalog_items_with_filters():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "hardware", "description": "d1", "active": True},
        {"item_id": "2", "name": "b", "category": "software", "description": "d2", "active": True}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(category="hardware")

    # Assert
    assert len(result.items) == 1
    assert result.items[0].category == "hardware"


def test_list_catalog_items_excludes_inactive_by_default():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "cat", "description": "d", "active": True},
        {"item_id": "2", "name": "b", "category": "cat", "description": "d", "active": False}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result.items) == 1
    assert result.items[0].item_id == "1"


def test_list_catalog_items_includes_inactive_when_flag_true():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "cat", "description": "d", "active": True},
        {"item_id": "2", "name": "b", "category": "cat", "description": "d", "active": False}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(include_inactive=True)

    # Assert
    assert len(result.items) == 2


def test_list_catalog_items_filters_and_inactive_combined():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "cat1", "description": "d", "active": True},
        {"item_id": "2", "name": "b", "category": "cat1", "description": "d", "active": False}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(category="cat1", include_inactive=False)

    # Assert
    assert len(result.items) == 1
    assert result.items[0].item_id == "1"


def test_list_catalog_items_returns_empty_when_no_match():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "cat1", "description": "d", "active": True}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(category="no-existe")

    # Assert
    assert result.items == []


def test_list_catalog_items_multiple_filters():
    # Arrange
    repo = Mock()
    repo.get.return_value = [
        {"item_id": "1", "name": "a", "category": "cat1", "unit": "kg", "active": True},
        {"item_id": "2", "name": "b", "category": "cat1", "unit": "lt", "active": True}
    ]

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(category="cat1", unit="kg")

    # Assert
    assert len(result.items) == 1
    assert result.items[0].item_id == "1"


def test_list_catalog_items_propagates_repo_exception():
    # Arrange
    repo = Mock()
    repo.get.side_effect = RuntimeError("db error")

    use_case = ListCatalogItems(repo)

    # Act & Assert
    with pytest.raises(RuntimeError, match="db error"):
        use_case.execute()