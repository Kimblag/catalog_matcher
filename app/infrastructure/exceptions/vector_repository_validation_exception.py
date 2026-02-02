from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


class VectorRepositoryValidationException(InfrastructureException):
    """Exception raised for validation errors in the Vector Repository."""

    def __init__(self, message: str):
        super().__init__(message)
