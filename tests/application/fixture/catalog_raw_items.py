from typing import Any
import pytest

@pytest.fixture
def raw_catalog_items_valid() -> list[dict[str, Any]]:
    return [
        {
            " item_id ": " ITEM-001 ",
            " name ": " Tornillo ",
            " category ": " Ferretería ",
            " description ": " Tornillo de acero ",
            " unit ": " unidad ",
            " provider ": " Acme ",
        },
        {
            " item_id ": " ITEM-002 ",
            " name ": " Tuerca ",
            " category ": " Ferretería ",
            " description ": " Tuerca hexagonal ",
        },
    ]


@pytest.fixture
def raw_catalog_items_missing_required_field(raw_catalog_items_valid):
    items = raw_catalog_items_valid.copy()
    broken = dict(items[0])
    broken.pop(" name ")
    items[0] = broken
    return items


@pytest.fixture
def raw_catalog_items_not_dict():
    return [
        "not a dict"
    ]

@pytest.fixture
def raw_catalog_items_invalid_value_type(raw_catalog_items_valid):
    items = raw_catalog_items_valid.copy()
    broken = dict(items[0])
    broken[" unit "] = 123
    items[0] = broken
    return items


@pytest.fixture
def raw_catalog_item_single():
    return [
        {
            " item_id ": " ITEM-001 ",
            " name ": " Tornillo ",
            " category ": " Ferretería ",
            " description ": " Tornillo de acero ",
        }
    ]
