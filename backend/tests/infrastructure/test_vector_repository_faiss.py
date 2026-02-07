from pathlib import Path

import faiss
import numpy as np
import pytest

from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import \
    VectorRepositoryFAISS
from app.infrastructure.exceptions.vector_repository_exception import VectorRepositoryException
from app.infrastructure.exceptions.vector_repository_validation_exception import VectorRepositoryValidationException
from tests.infrastructure.fixtures.raw_items import *

DIMENSION = 1536

def test_load_index_when_file_exists_should_load(tmp_path: Path):
    index_path = tmp_path / "index.index"
    # create empty index
    index = faiss.IndexFlatL2(DIMENSION)

    # create test vectors
    embeddings = np.random.rand(5, DIMENSION).astype(np.float32)
    index.add(embeddings)

    # save index
    faiss.write_index(index, str(index_path))

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)
    assert vector_repo.index.d == DIMENSION
    assert vector_repo.index.ntotal == 5


def test_load_index_when_file_not_exists_should_create(tmp_path: Path):
    index_path = tmp_path / "index_db.index"

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    assert vector_repo.index.d == DIMENSION
    assert vector_repo.index.ntotal == 0


def test_save_should_add_embeddings_and_persist(tmp_path: Path, raw_catalog_items_valid):
    index_path = tmp_path / "index_db.index"

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)   

    for item in raw_catalog_items_valid:
        item["embedding"] = np.random.rand(DIMENSION).astype(np.float32)

    vector_repo.save(raw_catalog_items_valid)

    assert vector_repo.index.d == DIMENSION
    assert vector_repo.index.ntotal == len(raw_catalog_items_valid)
    assert index_path.exists() == True


def test_save_with_empty_list_should_do_nothing(tmp_path: Path):
    index_path = tmp_path / "index.index"
    # create empty index
    index = faiss.IndexFlatL2(DIMENSION)

    # create test vectors
    embeddings = np.random.rand(5, DIMENSION).astype(np.float32)
    index.add(embeddings)

    # save index
    faiss.write_index(index, str(index_path))

    current_n_total = index.ntotal

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)   
    vector_repo.save([])
    
    assert vector_repo.index.ntotal == current_n_total
    assert index_path.exists() == True


def test_search_should_return_top_k_results_ordered_by_distance(tmp_path: Path, raw_catalog_items_valid):
    # Arrange
    index_path = tmp_path / "index_db.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    # Create deterministic embeddings
    for i, item in enumerate(raw_catalog_items_valid):
        # Vector con patrón predecible
        embedding = np.zeros(DIMENSION, dtype=np.float32)
        embedding[0] = float(i)  # Primer componente distingue cada vector
        item["embedding"] = embedding
    
    vector_repo.save(raw_catalog_items_valid)

    # Use first item's embedding as query (should match itself with distance ~0)
    query_embedding = raw_catalog_items_valid[0]["embedding"].tolist()
    top_k = 3

    # Act
    results = vector_repo.search(query_embedding, top_k)

    # Assert
    assert len(results) == min(top_k, len(raw_catalog_items_valid))
    
    first_id, first_dist = results[0]
    assert first_id == "ITEM-001"
    assert first_dist < 0.01  
    

    distances = [dist for _, dist in results]
    assert distances == sorted(distances)
    

    for item_id, dist in results:
        assert isinstance(item_id, str)
        assert item_id.startswith("ITEM-")
        assert isinstance(dist, float)
        assert dist >= 0.0


def test_search_with_wrong_dimension_should_raise(tmp_path: Path, raw_catalog_items_valid):
    index_path = tmp_path / "index_db.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    for item in raw_catalog_items_valid:
        item["embedding"] = np.random.rand(DIMENSION + 1).astype(np.float32)
    
    wrong_vector = raw_catalog_items_valid[0]["embedding"].tolist()

    with pytest.raises(VectorRepositoryValidationException, match="Invalid Vector dimension"):
        vector_repo.search(wrong_vector, top_k=3)

def test_search_when_top_k_exceeds_total_items_returns_all_available(tmp_path: Path):
    index_path = tmp_path / "index.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)
    
    items = [
        {"item_id": "A", "embedding": np.zeros(DIMENSION, dtype=np.float32)},
        {"item_id": "B", "embedding": np.ones(DIMENSION, dtype=np.float32)}
    ]
    vector_repo.save(items)
    
    results = vector_repo.search(np.zeros(DIMENSION).tolist(), top_k=10)
    
    assert len(results) == 2


def test_search_on_empty_index_returns_empty_list(tmp_path: Path):
    # Arrange
    index_path = tmp_path / "empty.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)
    
    # Act
    results = vector_repo.search(np.zeros(DIMENSION).tolist(), top_k=5)
    
    # Assert
    assert results == []

def test_search_returns_results_ordered_by_similarity(tmp_path: Path):
    # Arrange
    index_path = tmp_path / "index.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)
    
    query = np.zeros(DIMENSION, dtype=np.float32)
    query[0] = 1.0
    
    items = [
        {"item_id": "exact", "embedding": query.copy()},
        {"item_id": "close", "embedding": query + 0.1},
        {"item_id": "far", "embedding": np.ones(DIMENSION, dtype=np.float32) * 10}
    ]
    vector_repo.save(items)
    
    # Act
    results = vector_repo.search(query.tolist(), top_k=3)
    
    # Assert
    assert results[0][0] == "exact"
    assert results[1][0] == "close"
    assert results[2][0] == "far"
    
    assert results[0][1] < results[1][1] < results[2][1]