from collections.abc import Callable
from typing import Any

from .base import LLMResponse


class MockLLMProvider:
    """Deterministic provider for tests and local development without API calls."""

    def __init__(self, response_factory: Callable[[dict[str, Any]], dict[str, Any]] | None = None):
        self.response_factory = response_factory or (lambda payload: payload)

    def complete(self, system_prompt: str, payload: dict[str, Any]) -> LLMResponse:
        return LLMResponse(self.response_factory(payload), model="mock")