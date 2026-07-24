from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List


@dataclass
class Chunk:
    text: str
    file: str
    page: int
    chapter: str | None = None
    heading: str | None = None
    keywords: List[str] | None = None
    summary: str | None = None


class DocumentProcessor:
    """Document preprocessing utility for the modular RAG pipeline."""

    def clean_text(self, text: str) -> str:
        if not text:
            return ""

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def clean_text_pages(self, pages: List[dict[str, Any]]) -> List[dict[str, Any]]:
        cleaned_pages: List[dict[str, Any]] = []

        for page in pages:
            cleaned_text = self.clean_text(page.get("text", ""))
            if not cleaned_text:
                continue

            cleaned_pages.append({
                **page,
                "text": cleaned_text,
                "chapter": page.get("chapter"),
                "heading": page.get("heading"),
                "keywords": page.get("keywords", []),
                "summary": page.get("summary"),
            })

        return cleaned_pages

    def chunk(self, pages: List[dict[str, Any]]) -> List[Chunk]:
        chunks: List[Chunk] = []
        for page in pages:
            text = self.clean_text(page.get("text", ""))
            if not text:
                continue
            chunks.append(
                Chunk(
                    text=text,
                    file=page.get("file", "unknown.pdf"),
                    page=int(page.get("page", 1)),
                    chapter=page.get("chapter"),
                    heading=page.get("heading"),
                    keywords=page.get("keywords", []),
                    summary=page.get("summary"),
                )
            )
        return chunks