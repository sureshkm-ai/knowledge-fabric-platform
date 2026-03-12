from openai import AzureOpenAI

from src.llm.providers.base import BaseLLMProvider


class AzureOpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, endpoint: str, api_version: str, deployment: str = "gpt-4o-mini"):
        self.client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
        self.deployment = deployment

    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(model=self.deployment, messages=messages)
        return response.choices[0].message.content or ""
