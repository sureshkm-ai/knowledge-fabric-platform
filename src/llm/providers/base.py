"""Base LLM provider abstraction."""
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
        """Run completion."""


class MockLLMProvider(BaseLLMProvider):
    def invoke(self, prompt: str, system_prompt: str | None = None) -> str:
        return f"[MOCKED ANSWER] {prompt[:200]}"
