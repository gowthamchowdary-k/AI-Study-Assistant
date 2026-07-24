from __future__ import annotations

from formatter.response_formatter import ResponseFormatter
from intent.intent_router import IntentRouter
from prompts.prompt_manager import PromptManager
from rag.retriever import HybridRetriever
from services.rag_service import get_index, get_chunks
from services.chat_service import build_context


class LearningService:
    """Coordinates intent routing, retrieval, prompt selection, and structured output."""

    def __init__(self):
        self.intent_router = IntentRouter()
        self.prompt_manager = PromptManager()
        self.formatter = ResponseFormatter()

    def answer(self, question: str) -> dict:
        action = self.intent_router.classify(question)
        prompt = self.prompt_manager.get_prompt(action)
        index = get_index()
        chunks = get_chunks()
        retriever = HybridRetriever(index, chunks)
        results = retriever.retrieve(question, k=5)
        context, sources = build_context(results)

        return self.formatter.format(
            title=action.replace("_", " ").title(),
            answer=f"{prompt}\n\nContext:\n{context}",
            sources=sources,
            confidence=0.91 if results else 0.0,
            pages=[item["page"] for item in results],
            follow_up_questions=["What would you like to study next?"],
            study_tips=["Review the retrieved sources and test yourself with follow-up questions."],
        )
