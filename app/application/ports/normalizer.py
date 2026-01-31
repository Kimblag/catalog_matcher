from typing import Any, Protocol


class NormalizerCatalog(Protocol):

    def normalize_catalog_items(
        self,
        raw_items: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        ...


class NormalizerRequirement(Protocol):
    def normalize_requirements(
        self,
        raw_requirements: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        ...