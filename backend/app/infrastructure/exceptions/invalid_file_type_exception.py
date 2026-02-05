from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


class InvalidFileTypeException(InfrastructureException):
    """Exception raised for invalid file types."""

    def __init__(self, message: str):
        super().__init__(message)
