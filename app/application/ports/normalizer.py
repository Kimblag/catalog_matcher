from typing import Protocol


class NormalizerCatalog(Protocol):

    def normalize_catalog_items(
        self,
        raw_items: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        ...


class NormalizerRequirement(Protocol):
    def normalize_requirements(
        self,
        raw_requirements: list[dict[str, str]]
    ) -> list[dict[str, str]]:
        ...