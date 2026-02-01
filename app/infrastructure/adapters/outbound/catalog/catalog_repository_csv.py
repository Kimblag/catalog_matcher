import csv
import json
from pathlib import Path
from typing import Any

from app.application.ports.catalog_repository import CatalogRepository
from app.domain.entities.catalog import Catalog


class CatalogRepositoryCSV(CatalogRepository):

    _FIELDNAMES = [
        "item_id",
        "name",
        "category",
        "subcategory",
        "description",
        "unit",
        "provider",
        "attributes",
        "active",
    ]

    def __init__(self, csv_path: Path | None = None ) -> None:
        self.csv_path = csv_path or Path("data") / "catalog" / "catalog.csv"
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)


    def get(self) -> list[dict[str, Any]]:
        if not self.csv_path.exists():
            return []

        with open(self.csv_path, mode='r', encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            items = []
            for row in csv_reader:
                item = dict(row)

                if "attributes" in item:
                    attr_value = item["attributes"]
                    if attr_value:
                        try:
                            item["attributes"] = json.loads(attr_value)
                        except json.JSONDecodeError:
                            item["attributes"] = {}
                    else:
                        item["attributes"] = {}

                if "active" in item:
                    active_value = item["active"]
                    if active_value is None or active_value == "":
                        item["active"] = True
                    else:
                        item["active"] = active_value.lower() == "true"

                items.append(item)

            return items
    

    def save(self, catalog: list[dict[str, Any]]) -> None:
        with open(self.csv_path, mode='w', newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self._FIELDNAMES,
                extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(self._serialize_rows(catalog))

        
    def _serialize_rows(self, catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
        serialized = []

        for item in catalog:
            row = dict(item)

            # attributes -> json string
            attributes = row.get("attributes")
            if attributes is None or attributes == {}:
                row["attributes"] = "{}"
            else:
                row["attributes"] = json.dumps(attributes)

                # active -> string
                row["active"] = str(row.get("active", True)).lower()

            serialized.append(row)

        return serialized