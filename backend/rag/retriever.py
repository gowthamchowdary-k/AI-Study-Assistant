from __future__ import annotations

from typing import Any, Dict, List


class HybridRetriever:
    """A lightweight hybrid retrieval interface that preserves the current FAISS workflow."""

    def __init__(self, index: Any, chunks: List[Dict[str, Any]]):
        self.index = index
        self.chunks = chunks

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        if not self.index or not self.chunks:
            return []

        # Keep compatibility with the existing search pipeline by delegating to the current search function.
        from search import search_chunks

        return search_chunks(query, self.index, self.chunks, k=k)
