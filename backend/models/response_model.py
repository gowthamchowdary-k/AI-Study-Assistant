from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class LearningResponse:
    title: str = "Study Response"
    summary: str = ""
    sections: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    lists: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    confidence: float = 0.0
    pages: List[int] = field(default_factory=list)
    follow_up_questions: List[str] = field(default_factory=list)
    study_tips: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "sections": self.sections,
            "tables": self.tables,
            "lists": self.lists,
            "sources": self.sources,
            "confidence": self.confidence,
            "pages": self.pages,
            "follow_up_questions": self.follow_up_questions,
            "study_tips": self.study_tips,
        }
