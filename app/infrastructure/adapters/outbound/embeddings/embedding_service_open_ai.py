import openai

from app.application.ports.embedding_service import EmbeddingService
from app.infrastructure.config import settings
from app.infrastructure.exceptions.embedding_service_exception import EmbeddingServiceException


class OpenAIEmbeddingService(EmbeddingService):
    def __init__(self, model: str = settings.OPENAI_MODEL):
        self.model = model
        self.api_key = settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise EmbeddingServiceException("OPENAI_API_KEY is not set")
        
        openai.api_key = self.api_key


    def get_embedding(self, text: str) -> list[float]:
        if not text:
            raise EmbeddingServiceException("Input text cannot be empty")
        
        try:
            response = openai.embeddings.create(model=self.model, input=text)
            return response.data[0].embedding
        except openai.OpenAIError as e:
            raise EmbeddingServiceException(f"Failed to get embedding: {str(e)}") from e
        