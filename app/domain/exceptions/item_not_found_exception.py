from typing import Optional
from app.domain.exceptions.domain_exception import DomainException


class ItemNotFoundException(DomainException):
    __DEFAULT_MESSAGE: str = 'Item not found'

    def __init__(self, message: Optional[str] = None):
        self.message = message or ItemNotFoundException.__DEFAULT_MESSAGE
        super().__init__(self.message)