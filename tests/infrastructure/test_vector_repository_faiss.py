from pathlib import Path

import faiss
import numpy as np
import pytest

from app.infrastructure.adapters.outbound.vector_store.vector_repository_faiss import \
    VectorRepositoryFAISS
from tests.infrastructure.fixtures.raw_items import *


def test_load_index_when_file_exists_should_load(tmp_path: Path):
    index_path = tmp_path / "index.index"
    DIMENSION = 384
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
    DIMENSION = 384

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    assert vector_repo.index.d == DIMENSION
    assert vector_repo.index.ntotal == 0


def test_save_should_add_embeddings_and_persist(tmp_path: Path, raw_catalog_items_valid):
    index_path = tmp_path / "index_db.index"
    DIMENSION = 384

    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)   

    for item in raw_catalog_items_valid:
        item["embedding"] = np.random.rand(DIMENSION).astype(np.float32)

    vector_repo.save(raw_catalog_items_valid)

    assert vector_repo.index.d == DIMENSION
    assert vector_repo.index.ntotal == len(raw_catalog_items_valid)
    assert index_path.exists() == True


def test_save_with_empty_list_should_do_nothing(tmp_path: Path):
    index_path = tmp_path / "index.index"
    DIMENSION = 384
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


def test_search_should_return_top_k_results(tmp_path: Path, raw_catalog_items_valid):
    DIMENSION = 384
    index_path = tmp_path / "index_db.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    # arrange embeddings
    for item in raw_catalog_items_valid:
        item["embedding"] = np.random.rand(DIMENSION).astype(np.float32)
    vector_repo.save(raw_catalog_items_valid)

    # use the first embedding as query
    query_embedding = raw_catalog_items_valid[0]["embedding"].tolist()
    top_k = 3

    results = vector_repo.search(query_embedding, top_k)

    assert isinstance(results, list)
    assert len(results) == top_k
    for idx, dist in results:
        assert isinstance(idx, str)
        assert isinstance(dist, float)
        assert dist >= 0


def test_search_with_wrong_dimension_should_raise(tmp_path: Path, raw_catalog_items_valid):
    DIMENSION = 384
    index_path = tmp_path / "index_db.index"
    vector_repo = VectorRepositoryFAISS(dimension=DIMENSION, path=index_path)

    for item in raw_catalog_items_valid:
        item["embedding"] = np.random.rand(DIMENSION + 1).astype(np.float32)
    
    wrong_vector = raw_catalog_items_valid[0]["embedding"].tolist()

    with pytest.raises(ValueError, match="Invalid Vector dimension"):
        vector_repo.search(wrong_vector, top_k=3)