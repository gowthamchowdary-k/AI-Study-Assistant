from __future__ import annotations

from pyexpat import model
from typing import Any, Dict, Iterator, List

from google import genai

from config import GEMINI_API_KEY
from providers.base_provider import BaseProvider
from config import GEMINI_MODEL


class GeminiProvider(BaseProvider):
    """Gemini provider using the official google-genai SDK."""

    def __init__(self, api_key: str | None = None , model: str | None = None):
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

        self.model = model or GEMINI_MODEL
        self.client = genai.Client(api_key=api_key)
    
    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        prompt_parts: List[str] = []

        for message in messages:
            role = str(message.get("role", "user")).lower()
            content = str(message.get("content", "")).strip()

            if not content:
                continue

            if role == "system":
                prompt_parts.append(f"System:\n{content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant:\n{content}")
            else:
                prompt_parts.append(f"User:\n{content}")

        return "\n\n".join(prompt_parts)

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        try:
            prompt = self._messages_to_prompt(messages)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return getattr(response, "text", str(response))
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    def generate_stream(self, messages: List[Dict[str, Any]]) -> Iterator[str]:
        try:
            prompt = self._messages_to_prompt(messages)
            stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
            )

            for chunk in stream:
                text = getattr(chunk, "text", None)
                if text:
                    yield text
        except Exception as exc:
            raise RuntimeError(f"Gemini streaming failed: {exc}") from exc
