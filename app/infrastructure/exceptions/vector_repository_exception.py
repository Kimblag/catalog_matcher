from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


class VectorRepositoryException(InfrastructureException):
    """Base exception for Vector Repository errors."""

    def __init__(self, message: str):
        super().__init__(message)
