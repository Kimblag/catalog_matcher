import json
from pathlib import Path

import faiss
import numpy as np
from faiss import IndexFlatL2

from app.application.ports.vector_repository import VectorRepository
from app.infrastructure.exceptions.vector_repository_exception import (
    VectorRepositoryException,
)
from app.infrastructure.exceptions.vector_repository_validation_exception import VectorRepositoryValidationException


class VectorRepositoryFAISS(VectorRepository):

    def __init__(self, dimension: int, path: str | Path | None = None):
        self.dimension = dimension
        self.path = Path(path) if path else Path("data") / "vectors" / "catalog.index"
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.index = self._load_or_create_index()
        self.mapping_path = self.path.with_suffix(".json")
        self.index_to_item_id = self._load_mapping()

    def _load_or_create_index(self) -> IndexFlatL2:
        # If path exists try to read the index file
        if self.path.exists():
            try:
                return faiss.read_index(str(self.path))
            except Exception as e:
                raise VectorRepositoryException(
                    f"Failed to load FAISS index from {self.path}: {str(e)}"
                ) from e

        return faiss.IndexFlatL2(self.dimension)

    def _load_mapping(self):
        if self.mapping_path.exists():
            with open(self.mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self, items: list[dict]) -> None:
        if not items:
            return

        for item in items:
            if "embedding" not in item or "item_id" not in item:
                raise VectorRepositoryValidationException("Each item must have 'embedding' and 'item_id' fields")

        try:
            # Reset index
            self.index.reset()

            # add embeddings
            self.index.add(np.array([item["embedding"] for item in items], np.float32))

            # persist to disk
            faiss.write_index(self.index, str(self.path))

            # extract item_ids
            item_ids = [item["item_id"] for item in items]

            # persist mapping to disk
            with open(self.mapping_path, "w", encoding="utf-8") as f:
                json.dump(item_ids, f)

            # sync memory with disk
            self.index_to_item_id = item_ids

        except Exception as e:
            raise VectorRepositoryException(
                f"Failed to save FAISS index or mapping: {str(e)}"
            ) from e

    def search(
        self, query_embedding: list[float], top_k: int
    ) -> list[tuple[str, float]]:

        if len(query_embedding) != self.dimension:
            raise VectorRepositoryValidationException(
                f"Invalid Vector dimension. Expected dimension: {self.dimension}, got: {len(query_embedding)}"
            )

        q = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(q, top_k)

        results: list[tuple[str, float]] = []

        for idx, dist in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.index_to_item_id):
                results.append((self.index_to_item_id[idx], float(dist)))

        return results
