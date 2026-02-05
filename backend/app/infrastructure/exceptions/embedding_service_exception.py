from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)


class EmbeddingServiceException(InfrastructureException):
    """Exception raised for errors in the embedding service."""

    def __init__(self, message: str):
        super().__init__(message)
