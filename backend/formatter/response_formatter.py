from __future__ import annotations

from typing import Any, Dict, List


class ResponseFormatter:
    """Formats model responses into a structured learning-platform payload."""

    def format(
        self,
        title: str,
        answer: str,
        sources: List[str] | None = None,
        confidence: float = 0.0,
        pages: List[int] | None = None,
        follow_up_questions: List[str] | None = None,
        study_tips: List[str] | None = None,
        sections: List[Dict[str, Any]] | None = None,
        tables: List[Dict[str, Any]] | None = None,
        lists: List[str] | None = None,
    ) -> Dict[str, Any]:
        return {
            "title": title,
            "summary": answer,
            "sections": sections or [],
            "tables": tables or [],
            "lists": lists or [],
            "sources": sources or [],
            "confidence": confidence,
            "pages": pages or [],
            "follow_up_questions": follow_up_questions or [],
            "study_tips": study_tips or [],
        }
