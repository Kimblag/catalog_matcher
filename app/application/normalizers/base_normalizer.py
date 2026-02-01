from abc import ABC
from typing import Any, Type
import unicodedata
from app.application.ports.normalizer import Normalizer


class BaseNormalizer(Normalizer, ABC):
    _REQUIRED_FIELDS: set[str]
    _OPTIONAL_FIELDS: set[str]
    _EXCEPTION: Type[Exception]

    @property
    def _ALLOWED_FIELDS(self) -> set[str]:
        return self._REQUIRED_FIELDS | self._OPTIONAL_FIELDS

    def normalize(
        self,
        raw_items: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                raise self._EXCEPTION(
                    f"Item at index {index} is not a dictionary."
                )

            normalized.append(self._normalize_item(item, index))

        return normalized

    def _normalize_item(
        self,
        item: dict[str, Any],
        index: int
    ) -> dict[str, Any]:
        normalized_item: dict[str, Any] = {}

        for key, value in item.items():
            normalized_key = self._normalize_text(key)

            if normalized_key not in self._ALLOWED_FIELDS:
                raise self._EXCEPTION(
                    f"Item at index {index} contains unknown field '{key}'."
                )

            normalized_item[normalized_key] = (
                self._normalize_text(value)
                if isinstance(value, str)
                else value
            )

        missing = self._REQUIRED_FIELDS - normalized_item.keys()
        if missing:
            raise self._EXCEPTION(
                f"Item at index {index} is missing required fields: {missing}"
            )

        return normalized_item

    @staticmethod
    def _normalize_text(value: str) -> str:
        value = value.strip().lower()
        value = unicodedata.normalize("NFD", value)
        return "".join(
            char for char in value
            if not unicodedata.combining(char)
        )
