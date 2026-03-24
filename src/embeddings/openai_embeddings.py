<<<<<<< HEAD
"""OpenAI embeddings provider."""
from __future__ import annotations

=======
>>>>>>> main
from openai import OpenAI

from src.embeddings.base import BaseEmbeddingProvider


class OpenAIEmbeddingsProvider(BaseEmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
<<<<<<< HEAD
        self.client = OpenAI(api_key=api_key, timeout=60.0, max_retries=2)
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
=======
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
>>>>>>> main
        resp = self.client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in resp.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]
