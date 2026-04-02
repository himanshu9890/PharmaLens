"""Abstract LLM provider interface.

This exists in Phase 1 purely to lock in the abstraction boundary.
Concrete implementations (Ollama, Claude API) are added in Phase 3.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


class LLMProvider(ABC):
    """Base interface for all LLM backends used by PharmaLens."""

    @abstractmethod
    async def complete(self, prompt: str, max_tokens: int = 1024) -> LLMResponse:
        """Send a prompt and return the completion."""
        ...

    @abstractmethod
    async def classify(self, text: str, labels: list[str]) -> str:
        """Zero-shot classify text into one of the provided labels."""
        ...


class NullLLMProvider(LLMProvider):
    """Placeholder used during Phase 1 when no LLM is configured."""

    async def complete(self, prompt: str, max_tokens: int = 1024) -> LLMResponse:
        return LLMResponse(
            text="[LLM not configured — add ANTHROPIC_API_KEY or enable Ollama]",
            model="null",
        )

    async def classify(self, text: str, labels: list[str]) -> str:
        return labels[0] if labels else "unknown"
