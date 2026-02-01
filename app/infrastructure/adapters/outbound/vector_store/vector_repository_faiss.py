import json
from pathlib import Path

import faiss
import numpy as np
from faiss import IndexFlatL2

from app.application.ports.vector_repository import VectorRepository


class VectorRepositoryFAISS(VectorRepository):

    def __init__(self, dimension: int, path: str | Path  | None = None):
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
            except Exception:
                pass
        
        return faiss.IndexFlatL2(self.dimension)

    def _load_mapping(self):
        if self.mapping_path.exists():
            with open(self.mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    

    def save(self, items: list[dict]) -> None:
        if not items:
            return

        embeddings = np.array([item["embedding"] for item in items], np.float32)
        self.index.add(embeddings)
        faiss.write_index(self.index, str(self.path))

        self.index_to_item_id.extend([item["item_id"] for item in items])
        with open(self.mapping_path, "w", encoding="utf-8") as f:
            json.dump(self.index_to_item_id, f)


    def search(self, query_embedding: list[float], top_k: int) -> list[tuple[str, float]]:
        if len(query_embedding) != self.dimension:
            raise ValueError("Invalid Vector dimension")

        q = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(q, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.index_to_item_id):
                results.append((self.index_to_item_id[idx], float(dist)))
        return results