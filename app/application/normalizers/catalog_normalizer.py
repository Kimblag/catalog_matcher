from typing import Any
from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.ports.normalizer import NormalizerCatalog


class CatalogNormalizer(NormalizerCatalog):
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

    def normalize_catalog_items(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                raise CatalogNormalizationException(
                     f"Item at index {index} is not a dictionary."
                )
            normalized_item = self._normalize_item(item, index)
            normalized.append(normalized_item)
            
        return normalized

    
    def _normalize_item(self, item: dict[str, str], index: int) -> dict[str, str]:
        normalized_item: dict[str, str] = {}

        # normalize keys
        for key, value in item.items():
            # remove blanks and pass to lower case
            normalized_key = key.strip().lower()
            normalized_value = value.strip().lower() if isinstance(value, str) else value
            normalized_item[normalized_key] = normalized_value

        # Validate required fields
        missing = self._REQUIRED_FIELDS - normalized_item.keys()
        if missing:
            raise CatalogNormalizationException(
                f"Item at index {index} is missing required fields: {missing}"
                )

        return normalized_item


