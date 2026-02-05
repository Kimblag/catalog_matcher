from app.application.exceptions.application_layer_exception import ApplicationLayerException


class RequirementNormalizationException(ApplicationLayerException):
    def __init__(self, message: str):
        super().__init__(message)