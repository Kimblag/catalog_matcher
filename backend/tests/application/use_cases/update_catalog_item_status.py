from unittest.mock import Mock
import pytest

from app.application.use_cases.update_catalog_item_status import UpdateCatalogItemStatus
from app.domain.entities.catalog import Catalog
from app.domain.exceptions.item_not_found_exception import ItemNotFoundException


# HAppy path
def test_update_catalog_item_deactivate_happy_path():
    # Arrange
    catalog = Catalog()
    catalog.add_or_update_item(
        item_id="ITEM-001",
        name="Tornillo",
        category="Ferretería",
        description="Tornillo de acero",
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = UpdateCatalogItemStatus(catalog_repository=repo)

    # Act
    use_case.execute("ITEM-001", active=False)

    # Assert
    updated_catalog = repo.save.call_args[0][0]
    assert updated_catalog.items["ITEM-001"].active is False
    repo.save.assert_called_once()


def test_update_catalog_item_activate_happy_path():
    # Arrange
    catalog = Catalog()
    catalog.add_or_update_item(
        item_id="ITEM-001",
        name="Tornillo",
        category="Ferretería",
        description="Tornillo de acero",
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = UpdateCatalogItemStatus(catalog_repository=repo)

    # Act
    use_case.execute("ITEM-001", active=True)

    # Assert
    updated_catalog = repo.save.call_args[0][0]
    assert updated_catalog.items["ITEM-001"].active is True
    repo.save.assert_called_once()


# error path
def test_update_catalog_item_not_found():
    # Arrange
    catalog = Catalog()

    repo = Mock()
    repo.get.return_value = catalog

    use_case = UpdateCatalogItemStatus(catalog_repository=repo)

    # Act & Assert
    with pytest.raises(ItemNotFoundException):
        use_case.execute("ITEM-404", active=False)

    repo.save.assert_not_called()


def test_update_catalog_item_calls_repo_get_once():
    # Arrange
    catalog = Catalog()
    catalog.add_or_update_item(
        item_id="ITEM-001",
        name="Tornillo",
        category="Ferretería",
        description="Tornillo de acero",
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = UpdateCatalogItemStatus(catalog_repository=repo)

    # Act
    use_case.execute("ITEM-001", active=False)

    # Assert
    repo.get.assert_called_once()


def test_update_catalog_item_deactivate_calls_repo_save_once():
    # Arrange
    catalog = Catalog()
    catalog.add_or_update_item(
        item_id="ITEM-001",
        name="Tornillo",
        category="Ferretería",
        description="Tornillo de acero",
    )

    repo = Mock()
    repo.get.return_value = catalog

    use_case = UpdateCatalogItemStatus(catalog_repository=repo)

    # Act
    use_case.execute("ITEM-001", active=False)

    # Assert
    repo.save.assert_called_once()
