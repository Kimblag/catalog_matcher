import pytest

@pytest.fixture
def raw_catalog_items_valid() -> list[dict[str, str]]:
    return [
        {
            "item_id": "ITEM-001",
            "name": " Laptop Gamer ",
            "category": " Electronics ",
            "description": " High performance laptop "
        },
        {
            "item_id": "ITEM-002",
            "name": " Mechanical Keyboard ",
            "category": " Electronics ",
            "description": " RGB keyboard "
        }
    ]