from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple
from collections import defaultdict

logger = logging.getLogger(__name__)


class ContextBuilder:
    """Builds a clean, compressed prompt context from retrieved chunks."""

    def __init__(self, max_chunks: int = 6, max_chars: int = 6000):
        self.max_chunks = max_chunks
        self.max_chars = max_chars

    def _deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        ordered: List[Dict[str, Any]] = []

        for item in results:
            chunk_text = str(item.get("text", "")).strip()
            key = (
                item.get("file"),
                item.get("page"),
                chunk_text
            )

            if not chunk_text or key in seen:
                continue

            seen.add(key)
            ordered.append(item)

        return ordered

    def _compress(self, context: str) -> str:
        if len(context) <= self.max_chars:
            return context

        logger.warning("Context exceeded max size; truncating to keep prompt stable.")
        return context[: self.max_chars].rstrip() + "\n\n[Context truncated for prompt efficiency.]"

    def build(self, results: List[Dict[str, Any]]) -> Tuple[str, List[str], List[int], List[str]]:
        ordered_results = self._deduplicate(results)[: self.max_chunks]

        context_parts = []
        sources = []
        pages = []
        chunk_ids = []

        for item in ordered_results:

            chunk_text = str(item.get("text", "")).strip()
            if not chunk_text:
                continue

            chunk_id = str(item.get("chunk_id") or "chunk")
            file_name = str(item.get("file") or "unknown.pdf")
            page_number = int(item.get("page") or 1)

            context_parts.append(
                f"""
        Document: {file_name}
        Page: {page_number}
        Chunk ID: {chunk_id}

        {chunk_text}
        """
            )

            if file_name not in sources:
                sources.append(file_name)

            if page_number not in pages:
                pages.append(page_number)

            chunk_ids.append(chunk_id)

        context = "\n".join(context_parts)
        return self._compress(context), sources, pages, chunk_ids
