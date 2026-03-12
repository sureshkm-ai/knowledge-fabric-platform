from vertexai import init
from vertexai.generative_models import GenerativeModel

from src.llm.providers.base import BaseLLMProvider


class VertexProvider(BaseLLMProvider):
    def __init__(self, project_id: str, location: str, model_name: str = "gemini-1.5-pro") -> None:
        init(project=project_id, location=location)
        self.model = GenerativeModel(model_name)

    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
        merged = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(merged)
        return response.text or ""
