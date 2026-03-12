"""Environment profile definitions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    llm_provider: str
    embedding_provider: str
    vectorstore_provider: str
    sql_backend: str
    observability_backend: str


PROFILES: dict[str, ProfileConfig] = {
    "local": ProfileConfig(
        name="local",
        llm_provider="openai",
        embedding_provider="local_sentence_transformer",
        vectorstore_provider="faiss",
        sql_backend="duckdb",
        observability_backend="jsonl",
    ),
    "enterprise_openai": ProfileConfig(
        name="enterprise_openai",
        llm_provider="azure_openai",
        embedding_provider="openai",
        vectorstore_provider="qdrant",
        sql_backend="bigquery",
        observability_backend="bigquery",
    ),
    "enterprise_vertex": ProfileConfig(
        name="enterprise_vertex",
        llm_provider="vertex",
        embedding_provider="vertex",
        vectorstore_provider="pgvector",
        sql_backend="bigquery",
        observability_backend="cloud_logging",
    ),
}
