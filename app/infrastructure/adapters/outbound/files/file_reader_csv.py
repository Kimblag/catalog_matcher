import json
from csv import DictReader
from io import StringIO
from typing import Any

from app.application.ports.file_reader import FileReader
from app.infrastructure.exceptions.invalid_file_type_exception import InvalidFileTypeException


class FileReaderCSV(FileReader):

    def read_catalog(self, file_bytes: bytes) -> list[dict[str, Any]]:
        return self._read_file(file_bytes)

    def read_requirements(self, file_bytes: bytes) -> list[dict[str, Any]]:
        return self._read_file(file_bytes)

    def _read_file(self, file_bytes: bytes) -> list[dict[str, Any]]:
        try:
            file_str = file_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise InvalidFileTypeException("Invalid encoding for CSV file") from e
        
        file_like = StringIO(file_str)

        csv_reader = DictReader(file_like)
        items = []

        for row in csv_reader:
            item = dict(row)

            # parse attributes JSON
            if "attributes" in item and item["attributes"]:
                try:
                    item["attributes"] = json.loads(item["attributes"])
                except json.JSONDecodeError:
                    item["attributes"] = {}

            # parse active boolean
            if "active" in item:
                item["active"] = item["active"].lower() == "true"

            items.append(item)

        return items
