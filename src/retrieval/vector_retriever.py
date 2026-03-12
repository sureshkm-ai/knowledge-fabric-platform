from src.embeddings.base import BaseEmbeddingProvider
from src.vectorstore.base import BaseVectorStore, RetrievedDoc


class VectorRetriever:
    def __init__(self, embedding_provider: BaseEmbeddingProvider, vector_store: BaseVectorStore):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        q = self.embedding_provider.embed_query(query)
        return self.vector_store.query(q, top_k=top_k, filters=filters)
