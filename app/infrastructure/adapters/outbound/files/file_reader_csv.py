from csv import DictReader
from pathlib import Path
from typing import Any
from app.application.ports.file_reader import FileReader


class FileReaderCSV(FileReader):

    def read_catalog(self, file_path: str) -> list[dict[str, Any]]:
        dir_path = Path(file_path)
        
        # Check if exists
        if not dir_path.exists():
            return []
        
        return self._read_file(dir_path)


    def read_requirements(self, file_path: str) -> list[dict[str, Any]]:
        dir_path = Path(file_path)
        
        # Check if exists
        if not dir_path.exists():
            return []
        
        return self._read_file(dir_path)
        
    
    def _read_file(self, dir_path) -> list[dict[str, Any]]:
        with open(dir_path, mode="r", encoding="utf-8") as file:
            csv_reader = DictReader(file)
            return [dict(row) for row in csv_reader]