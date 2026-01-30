import pytest

from app.domain.entities.catalog_item import CatalogItem
from app.domain.exceptions.invalid_catalog_item_exception import InvalidCatalogItemException

def test_create_valid_item():
    # arrange & act
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # assert
    assert isinstance(item, CatalogItem)
    assert item.item_id == "123ABC"
    assert item.name == "WD40"
    assert item.category == "Lubricante"
    assert item.description == "Aceite multiuso"
    assert item.active is True
    assert item.subcategory == "Aceites"
    assert item.unit == "ml"
    assert item.provider == "WD"
    assert item.attributes == {"uso": "general", "olor": "neutral"}


def test_create_item_empty_id():
    # arrange & act & assert
    with pytest.raises(InvalidCatalogItemException):
        CatalogItem(
            item_id="",
            name="WD40",
            category="Lubricante",
            description="Aceite multiuso",
            active=True,
            subcategory="Aceites",
            unit="ml",
            provider="WD",
            attributes={"uso": "general", "olor": "neutral"}
        )


def test_create_item_empty_name():
    # arrange & act & assert
    with pytest.raises(InvalidCatalogItemException):
        CatalogItem(
            item_id="123ABC",
            name="",
            category="Lubricante",
            description="Aceite multiuso",
            active=True,
            subcategory="Aceites",
            unit="ml",
            provider="WD",
            attributes={"uso": "general", "olor": "neutral"}
        )

def test_active_inactive_item():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )
    deactivated_item = item.deactivate()

    # act
    activated_item = item.activate()

    # assert
    assert isinstance(activated_item, CatalogItem)
    assert deactivated_item.active is False
    assert activated_item.active is True

def test_activate_already_active():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # act
    already_active_item = item.activate()

    # assert
    assert item.active is True
    assert isinstance(already_active_item, CatalogItem)
    assert already_active_item.active is True

def test_deactivate_active_item():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # act
    deactivated_item = item.deactivate()

    # assert
    assert isinstance(deactivated_item, CatalogItem)
    assert deactivated_item.active is False
    assert item.active is True

def test_update_name_valid():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # act
    item_new_name = item.update_name(new_name="New Name")

    # assert
    assert isinstance(item_new_name, CatalogItem)
    assert item_new_name.name == "New Name"

def test_update_name_empty():
    # arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # act, assert
    with pytest.raises(InvalidCatalogItemException):
        invalid_item = item.update_name(new_name="")

def test_update_attributes():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    #Act
    updated_item = item.update_attributes({"color":"rojo"})

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.attributes == {"uso": "general", "olor": "neutral", "color": "rojo"}


def test_replace_attributes():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    #Act
    updated_item = item.replace_attributes({"color":"rojo"})

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.attributes == {"color": "rojo"}

def test_update_description():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # Act
    updated_item = item.update_description("Nueva descripcion")

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.description == "Nueva descripcion"


def test_update_category():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # Act
    updated_item = item.update_category("Nueva categoria")

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.category == "Nueva categoria"

def test_update_unit():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # Act
    updated_item = item.update_unit("lts")

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.unit == "lts"


def test_update_provider():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aceites",
        unit="ml",
        provider="W",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # Act
    updated_item = item.update_provider("WD")

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.provider == "WD"


def test_update_subcategory():
    # Arrange
    item = CatalogItem(
        item_id="123ABC",
        name="WD40",
        category="Lubricante",
        description="Aceite multiuso",
        active=True,
        subcategory="Aces",
        unit="ml",
        provider="WD",
        attributes={"uso": "general", "olor": "neutral"}
    )

    # Act
    updated_item = item.update_subcategory("Aceites")

    # Assert
    assert isinstance(updated_item, CatalogItem)
    assert updated_item.subcategory == "Aceites"


