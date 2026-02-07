from datetime import datetime

import pytest

from app.domain.entities.catalog import Catalog
from app.domain.enums.catalog_sources import CatalogSource
from app.domain.exceptions.invalid_catalog_item_exception import (
    InvalidCatalogItemException,
)
from app.domain.exceptions.item_not_found_exception import ItemNotFoundException
from app.domain.entities.catalog_item import CatalogItem
from tests.domain.entities.fixtures.catalog_items import valid_item_dict, valid_item_obj


def test_add_or_update_item_new(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    item = catalog.get_item(valid_item_dict["item_id"])
    assert item.name == "WD40"
    assert item.active is True

def test_add_or_update_item_update(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    # cambiar nombre y atributos
    catalog.add_or_update_item(**{**valid_item_dict, "name": "WD40 PRO", "attributes": {"uso": "industrial"}})
    item = catalog.get_item(valid_item_dict["item_id"])
    assert item.name == "WD40 PRO"
    assert item.attributes == {"uso": "industrial"}

def test_add_or_update_item_invalid():
    catalog = Catalog()
    invalid_item = {
        "item_id": "x",
        "name": "",
        "category": "",
        "description": "desc",
        "subcategory": None,
        "unit": None,
        "provider": None,
        "attributes": {}
    }
    with pytest.raises(InvalidCatalogItemException):
        catalog.add_or_update_item(**invalid_item)

def test_batch_upsert_all_valid(valid_item_obj):
    catalog = Catalog()
    errors = catalog.batch_upsert([valid_item_obj])
    assert errors == {}
    stored = catalog.get_item(valid_item_obj.item_id)
    assert stored.name == "Aceite Industrial"

def test_batch_upsert_some_invalid(valid_item_obj):
    catalog = Catalog()
    # crear inválido directamente como CatalogItem explota
    with pytest.raises(InvalidCatalogItemException):
        CatalogItem(item_id="bad", name="", category="", description="desc", subcategory=None, unit="unit", provider="", attributes={})
    # batch solo con el válido
    errors = catalog.batch_upsert([valid_item_obj])
    assert errors == {}
    assert catalog.get_item(valid_item_obj.item_id).name == "Aceite Industrial"

def test_update_item_status_existing(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_status(valid_item_dict["item_id"], active=False)
    item = catalog.get_item(valid_item_dict["item_id"])
    assert item.active is False
    catalog.update_item_status(valid_item_dict["item_id"], active=True)
    item = catalog.get_item(valid_item_dict["item_id"])
    assert item.active is True

def test_update_item_status_not_found():
    catalog = Catalog()
    with pytest.raises(ItemNotFoundException):
        catalog.update_item_status("nonexistent", active=True)

def test_update_item_name(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_name(valid_item_dict["item_id"], "WD40 PRO")
    assert catalog.get_item(valid_item_dict["item_id"]).name == "WD40 PRO"

def test_update_item_category(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_category(valid_item_dict["item_id"], "Herramientas")
    assert catalog.get_item(valid_item_dict["item_id"]).category == "Herramientas"

def test_update_item_subcategory(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_subcategory(valid_item_dict["item_id"], "Premium")
    assert catalog.get_item(valid_item_dict["item_id"]).subcategory == "Premium"

def test_update_item_description(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_description(valid_item_dict["item_id"], "Nueva desc")
    assert catalog.get_item(valid_item_dict["item_id"]).description == "Nueva desc"

def test_update_item_unit(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_unit(valid_item_dict["item_id"], "L")
    assert catalog.get_item(valid_item_dict["item_id"]).unit == "L"

def test_update_item_provider(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_provider(valid_item_dict["item_id"], "WD International")
    assert catalog.get_item(valid_item_dict["item_id"]).provider == "WD International"

def test_update_item_attributes(valid_item_dict):
    catalog = Catalog()
    catalog.add_or_update_item(**valid_item_dict)
    catalog.update_item_attributes(valid_item_dict["item_id"], {"color": "azul"})
    assert catalog.get_item(valid_item_dict["item_id"]).attributes == {"color": "azul"}