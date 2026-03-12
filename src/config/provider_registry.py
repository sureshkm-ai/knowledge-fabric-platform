"""Provider registry helpers."""
from src.config.settings import get_settings
from src.llm.factory import create_llm
from src.embeddings.factory import create_embeddings
from src.vectorstore.factory import create_vector_store


def create_runtime_components():
    settings = get_settings()
    return {
        "settings": settings,
        "llm": create_llm(settings.profile.llm_provider, settings),
        "embeddings": create_embeddings(settings.profile.embedding_provider, settings),
        "vectorstore": create_vector_store(settings.profile.vectorstore_provider, settings),
    }
