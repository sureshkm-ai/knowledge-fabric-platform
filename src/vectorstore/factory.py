from src.vectorstore.base import BaseVectorStore
from src.vectorstore.faiss_store import FaissVectorStore
from src.vectorstore.pgvector_store import PgVectorStore
from src.vectorstore.qdrant_store import QdrantVectorStore


def create_vector_store(provider_name: str, settings) -> BaseVectorStore:
    try:
        if provider_name == "qdrant":
            return QdrantVectorStore(settings.qdrant_url, settings.qdrant_api_key)
        if provider_name == "pgvector":
            return PgVectorStore(settings.pgvector_dsn)
    except Exception:
        return FaissVectorStore()
    return FaissVectorStore()
