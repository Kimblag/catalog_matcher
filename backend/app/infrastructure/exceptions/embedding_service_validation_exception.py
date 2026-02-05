from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


class EmbeddingServiceValidationException(InfrastructureException):
    """Exception raised for validation errors in the Embedding Service."""

    def __init__(self, message: str):
        super().__init__(message)
