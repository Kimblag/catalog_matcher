from app.application.exceptions.empty_requirement_file_exception import EmptyRequirementFileException
from app.application.ports.catalog_repository import CatalogRepository
from app.application.ports.embedding_service import EmbeddingService
from app.application.ports.file_reader import FileReader
from app.application.ports.normalizer import NormalizerRequirement
from app.application.ports.vector_repository import VectorRepository
from app.domain.entities.catalog import Catalog


class MatchRequirements:
    def __init__(self,
                 file_reader: FileReader,
                 normalizer: NormalizerRequirement,
                 catalog_repository: CatalogRepository,
                 embedding_service: EmbeddingService,
                 vector_repository: VectorRepository,
                 top_k: int = 3):
        self.file_reader = file_reader
        self.normalizer = normalizer
        self.catalog_repository = catalog_repository
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        self.top_k = top_k

    def execute(self, file_path: str) -> list[dict]:
        # read the requirement file
        raw_items = self.file_reader.read_requirements(file_path)
        
        if len(raw_items) == 0:
            raise EmptyRequirementFileException("Requirements does not contains any item.")

        # normalize the requirement file
        normalized_requirements = self.normalizer.normalize_requirements(raw_items)
        
        catalog: Catalog = self.catalog_repository.get()

        # Create embeddings
        matches_output = []

        for requirement in normalized_requirements:
            attributes_str = ",".join(f"{k}:{v}" for k, v in requirement.get('attributes', {}).items()) 
            
            text_to_embed = ( 
                f"name: {requirement.get('name', '')} | " 
                f"description: {requirement.get('description', '')} | " 
                f"category: {requirement.get('category', '')} | " 
                f"subcategory: {requirement.get('subcategory', '')} | " 
                f"quantity: {requirement.get('quantity', '')} | " 
                f"unit: {requirement.get('unit', '')} | " 
                f"priority: {requirement.get('priority', '')} | " 
                f"provider: {requirement.get('provider', '')} | " 
                f"attributes: {attributes_str}" 
                )
            
            embedding = self.embedding_service.get_embedding(text_to_embed)

            top_matches = self.vector_repository.search(
                query_embedding=embedding,
                top_k=self.top_k
            )

            enriched_matches = []

            for item_id, score in top_matches:
                item = catalog.get_item(item_id)

                enriched_matches.append({
                    "catalog_item_id": item.item_id,
                    "name": item.name,
                    "category": item.category,
                    "subcategory": item.subcategory,
                    "description": item.description,
                    "unit": item.unit,
                    "provider": item.provider,
                    "attributes": item.attributes,
                    "score": score
                })

            matches_output.append({
                "requirement": requirement,
                "matches": enriched_matches
            })

        return matches_output
