import pytest

from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.normalizers.catalog_normalizer import CatalogNormalizer
from tests.application.fixture.catalog_raw_items import *


def test_normalize_valid_single_item(raw_catalog_item_single):
    normalizer = CatalogNormalizer()
    result = normalizer.normalize(raw_catalog_item_single)
    
    assert len(result) == 1
    assert result[0]["item_id"] == "item-001"
    assert result[0]["name"] == "tornillo"
    assert result[0]["category"] == "ferreteria"
    assert result[0]["description"] == "tornillo de acero"
    assert result[0]["active"] is True  # o el valor que tenga en el fixture


def test_normalize_valid_multiple_items(raw_catalog_items_valid):
    normalizer = CatalogNormalizer()
    result = normalizer.normalize(raw_catalog_items_valid)
    
    assert len(result) == 2
    assert result[0]["item_id"] == "item-001"
    assert result[1]["item_id"] == "item-002"
    assert all("active" in item for item in result)


def test_normalize_includes_optional_fields(raw_catalog_items_valid):
    normalizer = CatalogNormalizer()
    result = normalizer.normalize(raw_catalog_items_valid)
    
    if "unit" in raw_catalog_items_valid[0]:
        assert "unit" in result[0]
        assert result[0]["unit"] == "unidad"
    if "provider" in raw_catalog_items_valid[0]:
        assert "provider" in result[0]
        assert result[0]["provider"] == "acme"


def test_normalize_text_lowercase_and_trim():
    normalizer = CatalogNormalizer()
    result = normalizer.normalize([{
        " Item_ID ": " ITEM-001 ",
        " Name ": " TORNILLO ",
        " Category ": " Ferretería ",
        " Description ": " Tornillo de acero ",
        " Active ": True
    }])
    
    assert result[0]["item_id"] == "item-001"
    assert result[0]["name"] == "tornillo"
    assert result[0]["category"] == "ferreteria"


def test_normalize_removes_accents():
    normalizer = CatalogNormalizer()
    result = normalizer.normalize([{
        "item_id": "001",
        "name": "tornillo",
        "category": "Ferretería",
        "description": "descripción",
        "active": True
    }])
    
    assert result[0]["category"] == "ferreteria"
    assert result[0]["description"] == "descripcion"


def test_normalize_empty_list():
    normalizer = CatalogNormalizer()
    result = normalizer.normalize([])
    
    assert result == []


def test_normalize_preserves_non_string_values(raw_catalog_items_invalid_value_type):
    normalizer = CatalogNormalizer()
    result = normalizer.normalize(raw_catalog_items_invalid_value_type)
    
    # Los valores no-string se preservan tal cual
    if "unit" in result[0]:
        assert isinstance(result[0]["unit"], int)


def test_normalize_missing_required_field(raw_catalog_items_missing_required_field):
    normalizer = CatalogNormalizer()
    
    with pytest.raises(CatalogNormalizationException, match="missing required fields"):
        normalizer.normalize(raw_catalog_items_missing_required_field)


def test_normalize_item_not_dict(raw_catalog_items_not_dict):
    normalizer = CatalogNormalizer()
    
    with pytest.raises(CatalogNormalizationException, match="not a dictionary"):
        normalizer.normalize(raw_catalog_items_not_dict)


def test_normalize_unknown_field():
    normalizer = CatalogNormalizer()
    
    with pytest.raises(CatalogNormalizationException, match="unknown field"):
        normalizer.normalize([{
            "item_id": "001",
            "name": "tornillo",
            "category": "ferretería",
            "description": "desc",
            "active": True,
            "campo_invalido": "valor"
        }])