from click import File
from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from app.infrastructure.config import settings

template_router = APIRouter(
    prefix="/templates",
    tags=["Templates"],
)


@template_router.get(
    "/catalog", status_code=status.HTTP_200_OK, response_class=FileResponse
)
def get_catalog_template():
    return FileResponse(
        path=settings.TEMPLATE_CATALOG,
        filename="catalog_template.csv",
        media_type="text/csv",
    )


@template_router.get(
    "/requirement", status_code=status.HTTP_200_OK, response_class=FileResponse
)
def get_requirement_template():
    return FileResponse(
        path=settings.TEMPLATE_REQUIREMENT,
        filename="requirements_template.csv",
        media_type="text/csv",
    )
