from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class LLMResponse:
    content: dict[str, Any]
    model: str
    input_tokens: int = 0
    output_tokens: int = 0


class LLMProvider(Protocol):
    def complete(self, system_prompt: str, payload: dict[str, Any]) -> LLMResponse:
        """Return structured content or raise a provider-specific exception."""