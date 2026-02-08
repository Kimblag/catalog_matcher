from typing import Annotated

from app.application.dto.catalog_dtos import (
    CatalogListDTO,
    CategoriesListDTO,
    ProvidersListDTO,
    SubcategoriesListDTO,
)
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.normalizer import Normalizer
from app.application.use_cases.list_catalog_items import ListCatalogItems
from app.application.use_cases.list_categories import ListCategories
from app.application.use_cases.list_providers import ListProviders
from app.application.use_cases.list_subcategories import ListSubcategories
from app.application.use_cases.update_catalog_item_status import UpdateCatalogItemStatus
from app.application.use_cases.upsert_catalog import UpsertCatalog
from app.infrastructure.adapters.inbound.api.dependencies import *
from app.infrastructure.adapters.inbound.api.schemas.update_catalog_item_status_dto import (
    UpdateCatalogItemStatusDTO,
)
from app.infrastructure.adapters.outbound import *
from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import (
    VectorRepositoryFAISS,
)
from app.infrastructure.utils.file_validation import validate_file_extension
from fastapi import APIRouter, Body, Depends, File, Path, Query, UploadFile, status

catalog_router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@catalog_router.get("", status_code=status.HTTP_200_OK, response_model=CatalogListDTO)
def list_catalog(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
    include_inactive: Annotated[bool, Query()] = False,
):
    use_case = ListCatalogItems(catalog_repository)

    return use_case.execute(
        include_inactive=include_inactive,
    )


@catalog_router.post("/items", status_code=status.HTTP_200_OK)
async def upsert_catalog(
    # background_tasks: BackgroundTasks,
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
    file_reader: Annotated[FileReaderCSV, Depends(get_file_reader)],
    normalizer: Annotated[Normalizer, Depends(get_catalog_normalizer)],
    vector_repository: Annotated[VectorRepositoryFAISS, Depends(get_vector_repository)],
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
    catalog_file: UploadFile = File(...),
):
    validate_file_extension(catalog_file)

    use_case = UpsertCatalog(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )

    file_bytes = await catalog_file.read()
    use_case.execute(file_bytes)
    # background_tasks.add_task(
    #     use_case.execute,
    #     file_bytes)

    return


@catalog_router.get(
    "/categories", status_code=status.HTTP_200_OK, response_model=CategoriesListDTO
)
def list_categories(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
):
    use_case = ListCategories(catalog_repository=catalog_repository)

    return use_case.execute()


@catalog_router.get(
    "/providers", status_code=status.HTTP_200_OK, response_model=ProvidersListDTO
)
def list_providers(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
):
    use_case = ListProviders(catalog_repository=catalog_repository)

    return use_case.execute()


@catalog_router.get(
    "/subcategories",
    status_code=status.HTTP_200_OK,
    response_model=SubcategoriesListDTO,
)
def list_subcategories(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
):
    use_case = ListSubcategories(catalog_repository=catalog_repository)

    return use_case.execute()


@catalog_router.patch("/items/{item_id}/status", status_code=status.HTTP_204_NO_CONTENT)
def update_catalog_item_status(
    item_id: Annotated[str, Path()],
    status: Annotated[UpdateCatalogItemStatusDTO, Body()],
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
):

    use_case = UpdateCatalogItemStatus(catalog_repository=catalog_repository)

    use_case.execute(item_id=item_id, active=status.active)
    return
