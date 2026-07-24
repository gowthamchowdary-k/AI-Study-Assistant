from __future__ import annotations

from config import AI_PROVIDER, GEMINI_API_KEY, OPENROUTER_API_KEY
from providers.base_provider import BaseProvider
from providers.gemini_provider import GeminiProvider
from providers.openrouter_provider import OpenRouterProvider


def get_provider() -> BaseProvider:
    """Return a provider instance based on the configured AI_PROVIDER environment value."""

    provider_name = (AI_PROVIDER or "openrouter").strip().lower()

    if provider_name == "gemini":
        return GeminiProvider(api_key=GEMINI_API_KEY)

    if provider_name == "openrouter":
        return OpenRouterProvider(api_key=OPENROUTER_API_KEY)

    raise ValueError(
        f"Unsupported AI provider '{provider_name}'. Supported providers: gemini, openrouter."
    )
