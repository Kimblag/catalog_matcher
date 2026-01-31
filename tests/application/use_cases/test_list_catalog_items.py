import pytest
from unittest.mock import Mock

from app.application.use_cases.list_catalog_items import ListCatalogItems
from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource


# Happy path
def test_list_catalog_items_happy_path():
    # Arrange
    catalog = Catalog(catalog_source=CatalogSource.MANUAL)
    catalog.add_or_update_item(
        item_id="1",
        name="item1",
        category="cat1",
        description="desc1"
    )
    catalog.add_or_update_item(
        item_id="2",
        name="item2",
        category="cat2",
        description="desc2"
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result.catalog) == 2
    assert all(item.active for item in result.catalog)


def test_list_catalog_items_with_filters():
    # Arrange
    catalog = Catalog(CatalogSource.CSV)
    catalog.add_or_update_item("1", "a", "hardware", "d1")
    catalog.add_or_update_item("2", "b", "software", "d2")

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(filters={"category": "hardware"})

    # Assert
    assert len(result.catalog) == 1
    assert result.catalog[0].category == "hardware"


def test_list_catalog_items_excludes_inactive_by_default():
    # Arrange
    catalog = Catalog(CatalogSource.JSON)
    catalog.add_or_update_item("1", "a", "cat", "d")
    catalog.add_or_update_item("2", "b", "cat", "d")
    catalog.deactivate_item("2")

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result.catalog) == 1
    assert result.catalog[0].item_id == "1"


def test_list_catalog_items_includes_inactive_when_flag_true():
    # Arrange
    catalog = Catalog(CatalogSource.JSON)
    catalog.add_or_update_item("1", "a", "cat", "d")
    catalog.add_or_update_item("2", "b", "cat", "d")
    catalog.deactivate_item("2")

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(include_inactive=True)

    # Assert
    assert len(result.catalog) == 2


def test_list_catalog_items_filters_and_inactive_combined():
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item("1", "a", "cat1", "d")
    catalog.add_or_update_item("2", "b", "cat1", "d")
    catalog.deactivate_item("2")

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(filters={"category": "cat1"}, include_inactive=False)

    # Assert
    assert len(result.catalog) == 1
    assert result.catalog[0].item_id == "1"


def test_list_catalog_items_returns_empty_when_no_match():
    # Arrange
    catalog = Catalog(CatalogSource.CSV)
    catalog.add_or_update_item("1", "a", "cat1", "d")

    repo = Mock()
    repo.get.return_value = catalog

    use_case = ListCatalogItems(repo)

    # Act
    result = use_case.execute(filters={"category": "no-existe"})

    # Assert
    assert result.catalog == []


def test_list_catalog_items_propagates_repo_exception():
    # Arrange
    repo = Mock()
    repo.get.side_effect = RuntimeError("db error")

    use_case = ListCatalogItems(repo)

    # Act & Assert
    with pytest.raises(RuntimeError):
        use_case.execute()
