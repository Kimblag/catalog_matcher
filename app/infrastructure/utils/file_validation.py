from pathlib import Path
from fastapi import UploadFile

from app.infrastructure.constants import ALLOWED_FILE_EXTENSIONS
from app.infrastructure.exceptions import InvalidFileTypeException


def validate_file_extension(file: UploadFile):
    # extract extension
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_FILE_EXTENSIONS:
        raise InvalidFileTypeException(
            f"Invalid file type: {extension}. Allowed types are: {', '.join(ALLOWED_FILE_EXTENSIONS)}"
        )
