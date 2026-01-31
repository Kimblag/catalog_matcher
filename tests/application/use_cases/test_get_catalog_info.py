import pytest
from unittest.mock import Mock
from datetime import datetime

from app.application.use_cases.get_catalog_info import GetCatalogInfo
from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource


# Happy path
def test_get_catalog_info_happy_path():
    # Arrange
    catalog = Catalog(catalog_source=CatalogSource.MANUAL)
    catalog.add_or_update_item(
        item_id="ITEM-001",
        name="tornillo",
        category="ferreteria",
        description="tornillo de acero"
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = GetCatalogInfo(catalog_repository=repo)

    # Act
    result = use_case.execute()

    # Assert
    last_updated, source, version = result

    assert isinstance(last_updated, datetime)
    assert source == "MANUAL"
    assert version == catalog.get_version()


def test_get_catalog_info_calls_repo_get_once():
    # Arrange
    catalog = Catalog(catalog_source=CatalogSource.JSON)

    repo = Mock()
    repo.get.return_value = catalog

    use_case = GetCatalogInfo(catalog_repository=repo)

    # Act
    use_case.execute()

    # Assert
    repo.get.assert_called_once()


def test_get_catalog_info_propagates_repo_exception():
    # Arrange
    repo = Mock()
    repo.get.side_effect = RuntimeError("database error")

    use_case = GetCatalogInfo(catalog_repository=repo)

    # Act & Assert
    with pytest.raises(RuntimeError):
        use_case.execute()
