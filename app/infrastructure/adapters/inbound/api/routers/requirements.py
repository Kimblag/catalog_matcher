from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse

from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.normalizer import Normalizer
from app.application.use_cases.match_requirements import MatchRequirements
from app.infrastructure.adapters.inbound.api.dependencies import *
from app.infrastructure.adapters.inbound.api.schemas.catalog import \
    CatalogListOut
from app.infrastructure.adapters.outbound import *
from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import \
    VectorRepositoryFAISS

requirement_router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"],
)


@requirement_router.post(
    "/match", status_code=status.HTTP_200_OK, response_class=JSONResponse
)
async def get_match(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
    file_reader: Annotated[FileReaderCSV, Depends(get_file_reader)],
    normalizer: Annotated[Normalizer, Depends(get_requirement_normalizer)],
    vector_repository: Annotated[VectorRepositoryFAISS, Depends(get_vector_repository)],
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
    requirement_file: UploadFile = File(...),
):
    matcher = MatchRequirements(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )

    matches = matcher.execute(file_bytes=await requirement_file.read())

    return JSONResponse(content=CatalogListOut(catalog=matches).model_dump())
