from typing import Any
from app.application.exceptions.requirement_normalization_exception import RequirementNormalizationException
from app.application.ports.normalizer import NormalizerRequirement


class RequirementNormalizer(NormalizerRequirement):
    _REQUIRED_FIELDS: set[str] = {
        "name",
        "quantity",
        "unit"
   }
    
    _OPTIONAL_FIELDS: set[str] = {
        "description",
        "category",
        "subcategory",
        "priority",
        "provider",
        "attributes"
    }

    def normalize_requirements(
        self,
        raw_requirements: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for index, item in enumerate(raw_requirements):
            if not isinstance(item, dict):
                raise RequirementNormalizationException(
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
            raise RequirementNormalizationException(
                f"Item at index {index} is missing required fields: {missing}"
                )

        return normalized_item