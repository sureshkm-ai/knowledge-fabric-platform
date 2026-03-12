from src.embeddings.base import BaseEmbeddingProvider
from src.embeddings.local_embeddings import LocalSentenceTransformerEmbeddings
from src.embeddings.openai_embeddings import OpenAIEmbeddingsProvider
from src.embeddings.vertex_embeddings import VertexEmbeddingsProvider


class DeterministicEmbeddingProvider(BaseEmbeddingProvider):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        base = float(sum(ord(c) for c in text) % 1000) / 1000.0
        return [base + i * 0.001 for i in range(16)]


def create_embeddings(provider_name: str, settings) -> BaseEmbeddingProvider:
    try:
        if provider_name == "openai" and settings.openai_api_key:
            return OpenAIEmbeddingsProvider(settings.openai_api_key)
        if provider_name == "vertex" and settings.vertex_project_id:
            return VertexEmbeddingsProvider(settings.vertex_project_id, settings.vertex_location)
        if provider_name == "local_sentence_transformer":
            return LocalSentenceTransformerEmbeddings()
    except Exception:
        return DeterministicEmbeddingProvider()
    return DeterministicEmbeddingProvider()
