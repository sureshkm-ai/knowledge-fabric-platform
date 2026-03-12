"""Pydantic settings for profile-aware configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.profiles import PROFILES, ProfileConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_profile: str = "local"
    openai_api_key: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-08-01-preview"
    vertex_project_id: str | None = None
    vertex_location: str = "us-central1"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    pgvector_dsn: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    duckdb_path: str = "data/local_warehouse.duckdb"
    observability_jsonl_path: str = "logs/traces.jsonl"

    default_region_scope: str = "US-SOUTH"
    default_business_unit: str = "snacks"

    @property
    def profile(self) -> ProfileConfig:
        if self.app_profile not in PROFILES:
            raise ValueError(f"Unknown profile: {self.app_profile}")
        return PROFILES[self.app_profile]


@lru_cache
def get_settings() -> Settings:
    return Settings()
