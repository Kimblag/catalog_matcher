import uuid
from typing import Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.exceptions.application_layer_exception import (
    ApplicationLayerException,
)
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.invalid_catalog_item_exception import (
    InvalidCatalogItemException,
)
from app.domain.exceptions.item_not_found_exception import ItemNotFoundException
from app.infrastructure.exceptions.embedding_service_validation_exception import (
    EmbeddingServiceValidationException,
)
from app.infrastructure.exceptions.infrastructure_exception import (
    InfrastructureException,
)
from app.infrastructure.exceptions.invalid_file_type_exception import (
    InvalidFileTypeException,
)
from app.infrastructure.exceptions.vector_repository_validation_exception import (
    VectorRepositoryValidationException,
)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable):
        correlation_id: str = str(uuid.uuid4())
        try:
            return await call_next(request)
        # Add custom error handling logic
        except ItemNotFoundException as exc:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "error_code": "item_not_found",
                    "message": str(exc),
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
        except InvalidCatalogItemException as exc:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                content={
                    "error_code": "invalid_catalog_item",
                    "message": str(exc),
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
        except ApplicationLayerException as exc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error_code": "application_error",
                    "message": str(exc),
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
        except (
            InvalidFileTypeException,
            EmbeddingServiceValidationException,
            VectorRepositoryValidationException,
        ) as exc:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error_code": "infrastructure_validation_error",
                    "message": str(exc),
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
        except InfrastructureException as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error_code": "infrastructure_error",
                    "message": str(exc),
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
        except ValidationError as exc:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error_code": "validation_error",
                    "message": "Input validation failed",
                    "details": exc.errors(),
                    "correlation_id": correlation_id,
                },
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error_code": "internal_server_error",
                    "message": "An unexpected error occurred",
                    "details": None,
                    "correlation_id": correlation_id,
                },
            )
