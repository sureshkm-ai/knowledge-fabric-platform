<<<<<<< HEAD
"""Azure OpenAI provider integration."""
from __future__ import annotations

=======
>>>>>>> main
from openai import AzureOpenAI

from src.llm.providers.base import BaseLLMProvider


class AzureOpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, endpoint: str, api_version: str, deployment: str = "gpt-4o-mini"):
<<<<<<< HEAD
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            timeout=60.0,
            max_retries=2,
        )
        self.deployment = deployment

    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
=======
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
        self.deployment = deployment

    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
>>>>>>> main
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
<<<<<<< HEAD
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
=======
        response = self.client.chat.completions.create(model=self.deployment, messages=messages)
>>>>>>> main
        return response.choices[0].message.content or ""
