from app.application.exceptions.catalog_normalization_exception import (
    CatalogNormalizationException,
)
from app.application.normalizers.base_normalizer import BaseNormalizer


class CatalogNormalizer(BaseNormalizer):
    _REQUIRED_FIELDS: set[str] = {
        "item_id",
        "name",
        "category",
        "description",
    }

    _OPTIONAL_FIELDS: set[str] = {
        "subcategory",
        "unit",
        "provider",
        "attributes",
    }

    _EXCEPTION = CatalogNormalizationException
