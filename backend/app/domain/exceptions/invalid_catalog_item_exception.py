from app.domain.exceptions.domain_exception import DomainException


class InvalidCatalogItemException(DomainException):
    def __init__(self,  message):
        self.message = message
        super().__init__(self.message)