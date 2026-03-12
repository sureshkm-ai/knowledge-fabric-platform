"""Factory for profile-selected LLM providers."""
from __future__ import annotations

from src.llm.providers.azure_openai_provider import AzureOpenAIProvider
from src.llm.providers.base import BaseLLMProvider, MockLLMProvider
from src.llm.providers.openai_provider import OpenAIProvider
from src.llm.providers.vertex_provider import VertexProvider


def create_llm(provider_name: str, settings) -> BaseLLMProvider:
    try:
        if provider_name == "openai" and settings.openai_api_key:
            return OpenAIProvider(settings.openai_api_key)

        if provider_name == "azure_openai" and settings.azure_openai_api_key and settings.azure_openai_endpoint:
            return AzureOpenAIProvider(
                api_key=settings.azure_openai_api_key,
                endpoint=settings.azure_openai_endpoint,
                api_version=settings.azure_openai_api_version,
            )

        if provider_name == "vertex" and settings.vertex_project_id:
            return VertexProvider(settings.vertex_project_id, settings.vertex_location)
    except Exception:
        return MockLLMProvider()

    return MockLLMProvider()
