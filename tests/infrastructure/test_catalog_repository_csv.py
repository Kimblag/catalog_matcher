import csv
import json
from pathlib import Path

import pytest

from app.infrastructure.adapters.outbound.catalog.catalog_repository_csv import CatalogRepositoryCSV

# file does not exists
def test_get_when_file_does_not_exist_returns_empty(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    result = repo.get()

    assert result == []

# file exists and has data
def test_get_when_file_exists_returns_rows(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "item_id",
                "name",
                "category",
                "subcategory",
                "description",
                "unit",
                "provider",
                "attributes",
                "active",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "item_id": "1",
                "name": "item",
                "category": "cat",
                "subcategory": "",
                "description": "desc",
                "unit": "",
                "provider": "",
                "attributes": "{}",
                "active": "true",
            }
        )

    repo = CatalogRepositoryCSV(csv_path=csv_path)

    result = repo.get()

    assert len(result) == 1
    assert result[0]["item_id"] == "1"
    assert result[0]["active"] == "true"


# empty file catalog
def test_save_when_catalog_is_empty_writes_header_only(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    repo.save([])

    with open(csv_path, encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1


def test_save_when_catalog_has_items_persists_rows(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    catalog = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
        }
    ]

    repo.save(catalog)

    rows = repo.get()

    assert len(rows) == 1
    assert rows[0]["item_id"] == "1"
    assert rows[0]["active"] == "true"

def test_save_should_ignore_extra_fields(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    catalog = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
            "unexpected": "boom",
        }
    ]

    repo.save(catalog)

    rows = repo.get()
    assert "unexpected" not in rows[0]


def test_save_should_serialize_attributes_as_json(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    catalog = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
            "attributes": {"a": "1", "b": "2"},
        }
    ]

    repo.save(catalog)
    rows = repo.get()

    attributes = rows[0]["attributes"]
    parsed = json.loads(attributes)

    assert parsed == {"a": "1", "b": "2"}


def test_save_should_default_active_to_true(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    catalog = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
        }
    ]

    repo.save(catalog)
    rows = repo.get()

    assert rows[0]["active"] == "true"


def test_get_after_save_returns_raw_storage_format(tmp_path: Path):
    csv_path = tmp_path / "catalog.csv"
    repo = CatalogRepositoryCSV(csv_path=csv_path)

    catalog = [
        {
            "item_id": "1",
            "name": "item",
            "category": "cat",
            "description": "desc",
            "attributes": {"x": "y"},
            "active": False,
        }
    ]

    repo.save(catalog)
    rows = repo.get()

    assert isinstance(rows[0]["attributes"], str)
    assert rows[0]["active"] in ("true", "false")
