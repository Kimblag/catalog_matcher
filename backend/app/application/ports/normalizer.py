from typing import Any, Protocol


class Normalizer(Protocol):

    def normalize(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]: ...
