"""Vertex text embedding provider."""
from __future__ import annotations

from vertexai import init
from vertexai.language_models import TextEmbeddingModel

from src.embeddings.base import BaseEmbeddingProvider


class VertexEmbeddingsProvider(BaseEmbeddingProvider):
    def __init__(self, project_id: str, location: str, model_name: str = "text-embedding-005"):
        init(project=project_id, location=location)
        self.model = TextEmbeddingModel.from_pretrained(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self.model.get_embeddings(texts)
        return [v.values for v in vectors]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]
