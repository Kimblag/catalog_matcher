from datetime import datetime

import pytest

from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource
from app.domain.exceptions.invalid_catalog_item_exception import \
    InvalidCatalogItemException
from app.domain.exceptions.item_not_found_exception import \
    ItemNotFoundException
from tests.domain.entities.fixtures.catalog_items import (base_catalog_item,
                                                          min_catalog_item)


# HAppy path
def test_add_or_update_item_new(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act
    catalog.add_or_update_item(**base_catalog_item)

    # Assert
    assert base_catalog_item["item_id"] in catalog.items
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.name == base_catalog_item["name"]
    assert item.category == base_catalog_item["category"]
    assert item.description == base_catalog_item["description"]
    assert item.subcategory == base_catalog_item["subcategory"]
    assert item.unit == base_catalog_item["unit"]
    assert item.provider == base_catalog_item["provider"]
    assert item.attributes == base_catalog_item["attributes"]
    assert item.active is True


def test_add_or_update_item_update(min_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    # add the first item
    catalog.add_or_update_item(**min_catalog_item)

    # Update the object
    min_catalog_item["attributes"] = {"color": "blue"}
    
    # Act
    catalog.add_or_update_item(**min_catalog_item)

    # Assert
    assert min_catalog_item["item_id"] in catalog.items
    item = catalog.items[min_catalog_item["item_id"]]
    assert item.name == min_catalog_item["name"]
    assert item.category == min_catalog_item["category"]
    assert item.description == min_catalog_item["description"]
    assert item.subcategory == min_catalog_item["subcategory"]
    assert item.unit == min_catalog_item["unit"]
    assert item.provider == min_catalog_item["provider"]
    assert item.attributes == {"color": "blue"}
    assert item.active is True


# invalid item
def test_add_or_update_item_invalid():
    catalog = Catalog(CatalogSource.MANUAL)
    invalid_item = {
        "item_id": "XXX",
        "name": "",
        "category": None,
        "description": "desc"
    }
    with pytest.raises(InvalidCatalogItemException):
        catalog.add_or_update_item(**invalid_item)


# batch all valid
def test_add_or_update_items_batch_all_valid(base_catalog_item, min_catalog_item):
    catalog = Catalog(CatalogSource.MANUAL)
    batch = [base_catalog_item.copy(), min_catalog_item.copy()]
    errors = catalog.batch_upsert(batch)
    assert errors == {}
    assert catalog.get_version() == 1
    for item in batch:
        stored = catalog.items[item["item_id"]]
        assert stored.name == item["name"]


# batch some invalid
def test_add_or_update_items_batch_some_invalid(base_catalog_item):
    catalog = Catalog(CatalogSource.MANUAL)
    batch = [
        base_catalog_item.copy(),
        {"item_id": "bad1", "name": "", "category": None}
    ]
    errors = catalog.batch_upsert(batch)
    assert "bad1" in errors
    assert "123ABC" in catalog.items
    assert catalog.get_version() == 1



def test_add_or_update_items_batch_all_invalid():
    catalog = Catalog(CatalogSource.MANUAL)
    batch = [
        {"item_id": "bad1", "name": "", "category": None},
        {"item_id": "bad2", "name": None, "category": None}
    ]
    errors = catalog.batch_upsert(batch)
    assert "bad1" in errors
    assert "bad2" in errors
    assert catalog.get_version() == 0
    assert catalog.items == {}


# activate existing item
def test_activate_item_existing(min_catalog_item):
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**min_catalog_item)
    
    catalog.deactivate_item(min_catalog_item["item_id"])
    item = catalog.items[min_catalog_item["item_id"]]
    assert item.active is False
    
    # Act
    catalog.activate_item(min_catalog_item["item_id"])
    
    # Assert
    activated_item = catalog.items[min_catalog_item["item_id"]]
    assert activated_item.active is True


# activate non-existent item
def test_activate_item_not_found():
    catalog = Catalog(CatalogSource.MANUAL)
    with pytest.raises(ItemNotFoundException):
        catalog.activate_item("non_existent_id")


# deactivate existing item
def test_deactivate_item_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    
    # Act
    catalog.deactivate_item(base_catalog_item["item_id"])
    
    # Assert
    deactivated_item = catalog.items[base_catalog_item["item_id"]]
    assert deactivated_item.active is False

# deactivate non-existent item
def test_deactivate_item_not_found():
    # arrange
    catalog = Catalog(CatalogSource.MANUAL)
    
    # Act & assert
    with pytest.raises(ItemNotFoundException):
        catalog.deactivate_item("non_existent_id")


# update existing item's name
def test_update_item_name_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_name = "WD40 PRO"

    # Act
    catalog.update_item_name(base_catalog_item["item_id"], new_name)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.name == new_name


# update item's name when item does not exist
def test_update_item_name_not_found():
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act & Assert
    with pytest.raises(ItemNotFoundException):
        catalog.update_item_name("non_existent_id", "New Name")


# update existing item's category
def test_update_item_category_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_category = "Herramientas"

    # Act
    catalog.update_item_category(base_catalog_item["item_id"], new_category)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.category == new_category


# update existing item's subcategory
def test_update_item_subcategory_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_subcategory = "Multiuso Premium"

    # Act
    catalog.update_item_subcategory(base_catalog_item["item_id"], new_subcategory)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.subcategory == new_subcategory


# update existing item's description
def test_update_item_description_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_description = "Aceite multiuso profesional"

    # Act
    catalog.update_item_description(base_catalog_item["item_id"], new_description)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.description == new_description


# update existing item's unit
def test_update_item_unit_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_unit = "L"

    # Act
    catalog.update_item_unit(base_catalog_item["item_id"], new_unit)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.unit == new_unit


# update existing item's provider
def test_update_item_provider_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_provider = "WD International"

    # Act
    catalog.update_item_provider(base_catalog_item["item_id"], new_provider)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.provider == new_provider


# update existing item's attributes
def test_update_item_attributes_existing(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)
    new_attributes = {"color": "blue", "uso": "industrial"}

    # Act
    catalog.update_item_attributes(base_catalog_item["item_id"], new_attributes)

    # Assert
    item = catalog.items[base_catalog_item["item_id"]]
    assert item.attributes == new_attributes


# get initial catalog version
def test_get_version_initial():
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act
    version = catalog.get_version()

    # Assert
    assert version == 0


# get catalog version after add
def test_get_version_after_add(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act
    catalog.add_or_update_item(**base_catalog_item)

    # Assert
    assert catalog.get_version() == 1


# get last updated datetime
def test_get_last_updated(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act
    catalog.add_or_update_item(**base_catalog_item)
    last_updated = catalog.get_last_updated()

    # Assert
    assert isinstance(last_updated, datetime)


# get catalog source
def test_get_source():
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)

    # Act
    source = catalog.get_source()

    # Assert
    assert source == CatalogSource.MANUAL.name


# get items returns copy
def test_get_items(base_catalog_item):
    # Arrange
    catalog = Catalog(CatalogSource.MANUAL)
    catalog.add_or_update_item(**base_catalog_item)

    # Act
    items = catalog.get_items()
    items.clear()

    # Assert
    assert len(catalog.items) == 1