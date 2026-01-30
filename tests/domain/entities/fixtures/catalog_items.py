import pytest
from app.domain.entities.catalog_item import CatalogItem

@pytest.fixture
def base_catalog_item() -> CatalogItem:
    return CatalogItem(
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

@pytest.fixture
def min_catalog_item() -> CatalogItem:
    return CatalogItem(
        item_id="456DEF",
        name="Silicona",
        category="Lubricante",
        description="Silicona en spray",
        active=True,
        subcategory=None,
        unit=None,
        provider=None,
        attributes={}
    )

@pytest.fixture

def alt_catalog_item() -> CatalogItem:
    return CatalogItem(
        item_id="789GHI",
        name="Aceite Industrial",
        category="Lubricante",
        description="Aceite pesado",
        active=True,
        subcategory="Aceites Pesados",
        unit="L",
        provider="IndusOil",
        attributes={"uso": "industrial", "viscosidad": "alta"}
    )