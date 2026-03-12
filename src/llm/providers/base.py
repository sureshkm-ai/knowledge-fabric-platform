"""Base LLM provider contract."""
from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        """Run completion and return assistant text."""


class MockLLMProvider(BaseLLMProvider):
    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        return f"[MOCKED ANSWER] {prompt[:min(220, max_tokens)]}"
