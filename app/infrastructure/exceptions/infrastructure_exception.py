class InfrastructureException(Exception):
    """Base exceptionfor infrastructure errors."""

    def __init__(self, message: str):
        super().__init__(message)
