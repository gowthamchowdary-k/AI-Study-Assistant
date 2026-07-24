from __future__ import annotations

from typing import Any, Dict, Iterator, List

from openai import OpenAI, RateLimitError

from config import OPENROUTER_API_KEY
from providers.base_provider import BaseProvider


class OpenRouterProvider(BaseProvider):
    """OpenRouter-backed provider using the OpenAI-compatible SDK."""

    def __init__(self, api_key: str | None = None, model: str = "openrouter/free"):
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found. Check your .env file.")

        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return response.choices[0].message.content
        except RateLimitError as exc:
            raise RuntimeError(
                "OpenRouter rate limit reached. Please try again in a moment."
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"OpenRouter generation failed: {exc}") from exc

    def generate_stream(self, messages: List[Dict[str, Any]]) -> Iterator[str]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )

            for chunk in stream:
                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):
                    yield chunk.choices[0].delta.content
        except RateLimitError as exc:
            raise RuntimeError(
                "OpenRouter rate limit reached. Please try again in a moment."
            ) from exc
        except Exception as exc:
            raise RuntimeError(f"OpenRouter streaming failed: {exc}") from exc
