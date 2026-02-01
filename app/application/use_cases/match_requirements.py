from typing import Any

from app.application.exceptions.empty_requirement_file_exception import (
    EmptyRequirementFileException,
)
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.embedding_service import EmbeddingService
from app.application.ports.file_reader import FileReader
from app.application.ports.normalizer import Normalizer
from app.application.ports.vector_repository import VectorRepository
from app.domain.entities.catalog import Catalog
from app.infrastructure.config import settings


class MatchRequirements:
    def __init__(
        self,
        file_reader: FileReader,
        normalizer: Normalizer,
        catalog_repository: CatalogRepository,
        embedding_service: EmbeddingService,
        vector_repository: VectorRepository,
        top_k: int = 5,
    ):
        self.file_reader = file_reader
        self.normalizer = normalizer
        self.catalog_repository = catalog_repository
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        self.top_k = top_k

    def execute(self, file_bytes: bytes) -> list[dict]:
        raw_items = self.file_reader.read_requirements(file_bytes)

        if not raw_items:
            raise EmptyRequirementFileException(
                "Requirements does not contain any item."
            )

        normalized_requirements = self.normalizer.normalize(raw_items=raw_items)

        catalog_items: list[dict[str, Any]] = self.catalog_repository.get()
        catalog = Catalog()
        catalog.batch_upsert(catalog_items)

        output = self._get_matches(
            normalized_requirements=normalized_requirements, catalog=catalog
        )

        return output

    def _get_matches(self, normalized_requirements, catalog):
        output = []

        for requirement in normalized_requirements:
            attributes_str = ",".join(
                f"{k}:{v}" for k, v in requirement.get("attributes", {}).items()
            )

            text_to_embed = (
                f"name: {requirement.get('name', '')} | "
                f"description: {requirement.get('description', '')} | "
                f"category: {requirement.get('category', '')} | "
                f"subcategory: {requirement.get('subcategory', '')} | "
                f"unit: {requirement.get('unit', '')} | "
                f"provider: {requirement.get('provider', '')} | "
                f"attributes: {attributes_str}"
            )

            embedding = self.embedding_service.get_embedding(text_to_embed)

            candidates = self.vector_repository.search(
                query_embedding=embedding,
                top_k=self.top_k,
            )

            matches = []

            for item_id, distance in candidates:
                if distance > settings.MAX_DISTANCE:
                    continue

                item = catalog.get_item(item_id)

                matches.append(
                    {
                        "catalog_item_id": item.item_id,
                        "name": item.name,
                        "category": item.category,
                        "subcategory": item.subcategory,
                        "description": item.description,
                        "unit": item.unit,
                        "provider": item.provider,
                        "attributes": item.attributes,
                        "score": distance,
                    }
                )

            # orden semántico explícito (menor distancia = mejor)
            matches.sort(key=lambda m: m["score"])

            output.append(
                {
                    "requirement": requirement,
                    "matches": matches,
                }
            )

        return output