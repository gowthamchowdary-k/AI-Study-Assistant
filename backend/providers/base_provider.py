from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List


class BaseProvider(ABC):
    """Abstract contract for all AI providers used by the study assistant."""

    @abstractmethod
    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """Generate a complete response for the provided message list."""

    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, Any]]) -> Iterator[str]:
        """Stream a response token-by-token for the provided message list."""
