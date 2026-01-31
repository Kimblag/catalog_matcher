from csv import DictWriter
from pathlib import Path

import pytest

from app.application.ports.file_reader import FileReader
from app.infrastructure.adapters.outbound.files.file_reader_csv import \
    FileReaderCSV


@pytest.fixture
def file_reader() -> FileReader:
    return FileReaderCSV()


def write_csv_file(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.touch()
        return
    fieldnames = list(rows[0].keys())
    with open(path, mode="w", encoding="utf-8", newline="") as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)



def test_read_catalog_file_exists_should_return_rows(file_reader, tmp_path):
    file_path = tmp_path / "catalog.csv"
    rows = [
        {"item_id": "1", "name": "Item 1", "category": "Cat A", "description": "Desc"},
        {"item_id": "2", "name": "Item 2", "category": "Cat B", "description": "Desc"},
    ]
    write_csv_file(file_path, rows)

    result = file_reader.read_catalog(str(file_path))
    assert result == rows


def test_read_catalog_file_does_not_exist_should_return_empty(file_reader, tmp_path):
    file_path = tmp_path / "nonexistent.csv"
    result = file_reader.read_catalog(str(file_path))
    assert result == []


def test_read_catalog_file_empty_should_return_empty(file_reader, tmp_path):
    file_path = tmp_path / "empty.csv"
    write_csv_file(file_path, [])
    result = file_reader.read_catalog(str(file_path))
    assert result == []



def test_read_requirements_file_exists_should_return_rows(file_reader, tmp_path):
    file_path = tmp_path / "requirements.csv"
    rows = [
        {"name": "Req 1", "quantity": "10", "unit": "kg"},
        {"name": "Req 2", "quantity": "5", "unit": "l"},
    ]
    write_csv_file(file_path, rows)

    result = file_reader.read_requirements(str(file_path))
    assert result == rows


def test_read_requirements_file_does_not_exist_should_return_empty(file_reader, tmp_path):
    file_path = tmp_path / "nonexistent_reqs.csv"
    result = file_reader.read_requirements(str(file_path))
    assert result == []


def test_read_requirements_file_empty_should_return_empty(file_reader, tmp_path):
    file_path = tmp_path / "empty_reqs.csv"
    write_csv_file(file_path, [])
    result = file_reader.read_requirements(str(file_path))
    assert result == []



def test_read_file_returns_dict_rows(file_reader, tmp_path):
    file_path = tmp_path / "file.csv"
    rows = [
        {"item_id": "1", "name": "A", "category": "C", "description": "D"}
    ]
    write_csv_file(file_path, rows)

    # Usamos método interno directamente
    result = file_reader._read_file(file_path)
    assert all(isinstance(row, dict) for row in result)
    assert result == rows
