import pytest

from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.normalizers.catalog_normalizer import CatalogNormalizer
from tests.application.fixture.catalog_raw_items import *


# Happy path

def test_normalize_valid_single_item(raw_catalog_item_single):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_item_single)

    # Assert
    assert result == [
        {
            "item_id": "item-001",
            "name": "tornillo",
            "category": "ferretería",
            "description": "tornillo de acero",
        }
    ]


def test_normalize_valid_multiple_items(raw_catalog_items_valid):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_items_valid)

    # Assert
    assert len(result) == 2
    assert result[0]["item_id"] == "item-001"
    assert result[1]["item_id"] == "item-002"


def test_normalize_ignores_optional_fields(raw_catalog_items_valid):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_items_valid)

    # Assert
    assert "unit" in result[0]
    assert "provider" in result[0]
    assert result[0]["unit"] == "unidad"
    assert result[0]["provider"] == "acme"


def test_normalize_trims_and_lowercases_keys(raw_catalog_item_single):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_item_single)

    # Assert
    assert "item_id" in result[0]
    assert " item_id " not in result[0]


def test_normalize_trims_and_lowercases_values(raw_catalog_item_single):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_item_single)

    # Assert
    assert result[0]["name"] == "tornillo"


def test_normalize_empty_raw_items_list():
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items([])

    # Assert
    assert result == []


def test_normalize_attributes_non_string(raw_catalog_items_invalid_value_type):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act
    result = normalizer.normalize_catalog_items(raw_catalog_items_invalid_value_type)

    # Assert
    assert isinstance(result[0]["unit"], int)


# Error path

def test_normalize_missing_required_field(raw_catalog_items_missing_required_field):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act & Assert
    with pytest.raises(CatalogNormalizationException):
        normalizer.normalize_catalog_items(raw_catalog_items_missing_required_field)


def test_normalize_item_not_dict(raw_catalog_items_not_dict):
    # Arrange
    normalizer = CatalogNormalizer()

    # Act & Assert
    with pytest.raises(CatalogNormalizationException):
        normalizer.normalize_catalog_items(raw_catalog_items_not_dict)