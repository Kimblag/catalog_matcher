from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status

from app.application.dto.match_dtos import MatchResultDTO
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.normalizer import Normalizer
from app.application.use_cases.match_requirements import MatchRequirements
from app.infrastructure.adapters.inbound.api.dependencies import *
from app.infrastructure.adapters.outbound import *
from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import (
    VectorRepositoryFAISS,
)
from app.infrastructure.utils.file_validation import validate_file_extension

requirement_router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"],
)


@requirement_router.post(
    "/matches", status_code=status.HTTP_200_OK, response_model=MatchResultDTO
)
async def match(
    catalog_repository: Annotated[CatalogRepository, Depends(get_catalog_repository)],
    file_reader: Annotated[FileReaderCSV, Depends(get_file_reader)],
    normalizer: Annotated[Normalizer, Depends(get_requirement_normalizer)],
    vector_repository: Annotated[VectorRepositoryFAISS, Depends(get_vector_repository)],
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
    requirement_file: UploadFile = File(...),
):
    validate_file_extension(requirement_file)
    
    use_case = MatchRequirements(
        file_reader=file_reader,
        normalizer=normalizer,
        catalog_repository=catalog_repository,
        vector_repository=vector_repository,
        embedding_service=embedding_service,
    )
    return use_case.execute(file_bytes=await requirement_file.read())