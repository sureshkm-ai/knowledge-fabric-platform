<<<<<<< HEAD
"""Vertex AI Gemini provider integration."""
from __future__ import annotations

from vertexai import init
from vertexai.generative_models import GenerationConfig, GenerativeModel
=======
from vertexai import init
from vertexai.generative_models import GenerativeModel
>>>>>>> main

from src.llm.providers.base import BaseLLMProvider


class VertexProvider(BaseLLMProvider):
    def __init__(self, project_id: str, location: str, model_name: str = "gemini-1.5-pro") -> None:
        init(project=project_id, location=location)
        self.model = GenerativeModel(model_name)

<<<<<<< HEAD
    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        merged = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(
            merged,
            generation_config=GenerationConfig(temperature=temperature, max_output_tokens=max_tokens),
        )
=======
    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
        merged = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(merged)
>>>>>>> main
        return response.text or ""
