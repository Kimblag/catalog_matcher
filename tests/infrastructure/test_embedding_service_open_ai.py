import pytest
from unittest.mock import patch, MagicMock
import os

from app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai import OpenAIEmbeddingService




@pytest.fixture
def mock_env_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key-12345")


@pytest.fixture
def embedding_service(mock_env_api_key):
    return OpenAIEmbeddingService()


def test_init_with_default_model(mock_env_api_key):
    service = OpenAIEmbeddingService()
    
    assert service.model == "text-embedding-3-small"
    assert service.api_key == "test-api-key-12345"


def test_init_with_custom_model(mock_env_api_key):
    custom_model = "text-embedding-3-large"
    service = OpenAIEmbeddingService(model=custom_model)
    
    assert service.model == custom_model
    assert service.api_key == "test-api-key-12345"


def test_init_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        OpenAIEmbeddingService()


def test_init_sets_openai_api_key(mock_env_api_key):
    with patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai') as mock_openai:
        service = OpenAIEmbeddingService()
        
        assert mock_openai.api_key == "test-api-key-12345"


@patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai.embeddings.create')
def test_get_embedding_success(mock_create, embedding_service):
    # Arrange
    test_text = "This is a test text"
    expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=expected_embedding)]
    mock_create.return_value = mock_response
    
    # Act
    result = embedding_service.get_embedding(test_text)
    
    # Assert
    assert result == expected_embedding
    mock_create.assert_called_once_with(
        model="text-embedding-3-small",
        input=test_text
    )


@patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai.embeddings.create')
def test_get_embedding_with_custom_model(mock_create, mock_env_api_key):
    # Arrange
    custom_model = "text-embedding-3-large"
    service = OpenAIEmbeddingService(model=custom_model)
    test_text = "Test text"
    expected_embedding = [0.1, 0.2, 0.3]
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=expected_embedding)]
    mock_create.return_value = mock_response
    
    # Act
    result = service.get_embedding(test_text)
    
    # Assert
    assert result == expected_embedding
    mock_create.assert_called_once_with(
        model=custom_model,
        input=test_text
    )


@patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai.embeddings.create')
def test_get_embedding_with_empty_string(mock_create, embedding_service):
    # Arrange
    test_text = ""
    expected_embedding = [0.0, 0.0, 0.0]
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=expected_embedding)]
    mock_create.return_value = mock_response
    
    # Act
    result = embedding_service.get_embedding(test_text)
    
    # Assert
    assert result == expected_embedding
    mock_create.assert_called_once_with(
        model="text-embedding-3-small",
        input=test_text
    )


@patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai.embeddings.create')
def test_get_embedding_api_error(mock_create, embedding_service):
    # Arrange
    test_text = "Test text"
    mock_create.side_effect = Exception("API Error: Rate limit exceeded")
    
    # Act & Assert
    with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
        embedding_service.get_embedding(test_text)


@patch('app.infrastructure.adapters.outbound.embeddings.embedding_service_open_ai.openai.embeddings.create')
def test_get_embedding_returns_list_of_floats(mock_create, embedding_service):
    # Arrange
    test_text = "Test text"
    expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=expected_embedding)]
    mock_create.return_value = mock_response
    
    # Act
    result = embedding_service.get_embedding(test_text)
    
    # Assert
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    assert len(result) == len(expected_embedding)


def test_service_implements_protocol(embedding_service):
    from app.application.ports.embedding_service import EmbeddingService
    
    assert hasattr(embedding_service, 'get_embedding')
    assert callable(embedding_service.get_embedding)