import pytest
from app.domain.entities.catalog_item import CatalogItem


@pytest.fixture
def valid_item_dict():
    return {
        "item_id": "1",
        "name": "WD40",
        "category": "Lubricante",
        "description": "Aceite multiuso",
        "subcategory": "Aceites",
        "unit": "ml",
        "provider": "WD",
        "attributes": {"uso": "general"},
    }

@pytest.fixture
def valid_item_obj():
    return CatalogItem(
        item_id="2",
        name="Aceite Industrial",
        category="Lubricante",
        description="Aceite pesado",
        subcategory="Aceites Pesados",
        unit="L",
        provider="IndusOil",
        attributes={"uso": "industrial"}
    )