from __future__ import annotations

import re
from typing import Dict


class IntentRouter:
    """Classifies a user prompt into an action id for the learning platform."""

    ACTION_KEYWORDS: Dict[str, list[str]] = {
        "generate_mcqs": ["quiz", "mcq", "multiple choice", "questions"],
        "summary": ["summarize", "summary", "overview", "executive summary"],
        "explain": ["explain", "what is", "why", "how does", "describe"],
        "flashcards": ["flashcard", "flashcards", "memorize", "recall"],
        "revision": ["revision", "quick revision", "last minute", "cram"],
        "formula_sheet": ["formula", "equation", "derivation", "formula sheet"],
        "interview": ["interview", "viva", "oral", "defend"],
        "mindmap": ["mind map", "concept map", "diagram"],
        "study_plan": ["study plan", "schedule", "revision plan", "prepare for exam"],
        "comparison": ["compare", "difference between", "contrast"],
        "notes": ["notes", "chapter notes", "important topics"],
    }

    def classify(self, question: str) -> str:
        cleaned = re.sub(r"\s+", " ", question.strip().lower())
        if not cleaned:
            return "general"

        for action, keywords in self.ACTION_KEYWORDS.items():
            if any(keyword in cleaned for keyword in keywords):
                return action

        return "general"
