from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, UploadFile, status

from app.application.dto.catalog_dtos import CatalogListDTO
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.normalizer import Normalizer
from app.application.use_cases.upsert_catalog import UpsertCatalog
from app.application.use_cases.list_catalog_items import ListCatalogItems
from app.infrastructure.adapters.inbound.api.dependencies import *
from app.infrastructure.adapters.outbound import *
from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import \
    VectorRepositoryFAISS
from app.infrastructure.utils.file_validation import validate_file_extension

catalog_router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@catalog_router.get("/", status_code=status.HTTP_200_OK, response_model=CatalogListDTO)
def list_catalog(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
    category: Annotated[str | None, Query()] = None,
    subcategory: Annotated[str | None, Query()] = None,
    unit: Annotated[str | None, Query()] = None,
    provider: Annotated[str | None, Query()] = None,
    include_inactive: Annotated[bool, Query()] = False,
):
    use_case = ListCatalogItems(catalog_repository)

    return use_case.execute(
        category=category,
        subcategory=subcategory,
        unit=unit,
        provider=provider,
        include_inactive=include_inactive,
    )


@catalog_router.post("/items", status_code=status.HTTP_202_ACCEPTED)
async def upsert_catalog(
    background_tasks: BackgroundTasks,
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
    background_tasks.add_task(
        use_case.execute, 
        file_bytes)

    return
