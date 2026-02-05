from typing import Optional
from app.application.exceptions.application_layer_exception import ApplicationLayerException


class UnsupportedCatalogSourceException(ApplicationLayerException):
    __BASE_MESSAGE: str = f'Unsupported file extension: '

    def __init__(self, extension: str, message: Optional[str] = None):
        self.message = message or f"{self.__BASE_MESSAGE}: {extension}"
        super().__init__(self.message)