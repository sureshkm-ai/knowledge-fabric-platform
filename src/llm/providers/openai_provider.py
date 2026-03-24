<<<<<<< HEAD
"""OpenAI provider integration."""
from __future__ import annotations

=======
>>>>>>> main
from openai import OpenAI

from src.llm.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
<<<<<<< HEAD
        self.client = OpenAI(api_key=api_key, timeout=60.0, max_retries=2)
        self.model = model

    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
=======
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
>>>>>>> main
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
<<<<<<< HEAD
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
=======
        response = self.client.chat.completions.create(model=self.model, messages=messages)
>>>>>>> main
        return response.choices[0].message.content or ""
