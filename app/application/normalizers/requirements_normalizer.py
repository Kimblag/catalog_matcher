from app.application.exceptions.requirement_normalization_exception import (
    RequirementNormalizationException,
)
from app.application.normalizers.base_normalizer import BaseNormalizer


class RequirementNormalizer(BaseNormalizer):
    _REQUIRED_FIELDS: set[str] = {"name", "quantity", "unit"}

    _OPTIONAL_FIELDS: set[str] = {
        "description",
        "category",
        "subcategory",
        "priority",
        "provider",
        "attributes",
    }

    _EXCEPTION = RequirementNormalizationException
