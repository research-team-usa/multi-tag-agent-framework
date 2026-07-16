"""LLM client interface – für echte KI später."""

from abc import ABC, abstractmethod
from typing import Any


class LLMClient(ABC):
    """Abstract LLM client."""

    @abstractmethod
    def complete(self, message: str, context: str) -> Any:
        """Return completion for message."""
        raise NotImplementedError
