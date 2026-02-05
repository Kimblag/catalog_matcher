from typing import Any, Protocol


class FileReader(Protocol):
    def read_catalog(self, file_bytes: bytes) -> list[dict[str, Any]]:
        """
        Returns a list of raw catalog items.
        Each dict represents a row with primitive values only.
        """
        ...


    def read_requirements(self, file_bytes: bytes) -> list[dict[str, Any]]:
        """
        Returns a list of raw requirements.
        Each dict represents a row with primitive values only.
        """
        ...