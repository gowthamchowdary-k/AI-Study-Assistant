from __future__ import annotations

from typing import Dict


class PromptManager:
    """Maps learning actions to reusable prompt templates and injects context per request."""

    TEMPLATES: Dict[str, str] = {
        "summary": "You are a precise academic summarizer. Use ONLY the retrieved document context. Return an executive summary, key concepts, definitions, important formulae, examples, applications, and key takeaways.",
        "notes": "You are a subject-matter tutor. Use ONLY the retrieved document context. Produce clean chapter notes with definition, explanation, example, diagram suggestion, advantages, disadvantages, applications, and exam tips.",
        "generate_mcqs": "You are a quiz generator. Use ONLY the retrieved document context. Generate high-quality MCQs with 4 options, correct answer, explanation, difficulty, topic, and page reference.",
        "flashcards": "You are a flashcard designer. Use ONLY the retrieved document context. Produce front/back cards with difficulty, topic, and page reference.",
        "quiz": "You are an interactive quiz coach. Use ONLY the retrieved document context. Ask one question at a time, give hints if needed, and explain after each answer.",
        "revision": "You are a revision assistant. Use ONLY the retrieved document context. Produce one-page notes, quick facts, mnemonics, memory tricks, and last-minute revision bullets.",
        "formula_sheet": "You are a formula extraction assistant. Use ONLY the retrieved document context. Extract formulas, explain variables, explain usage, and provide solved examples.",
        "interview": "You are an interview coach. Use ONLY the retrieved document context. Simulate an interview, ask one question at a time, evaluate answers, and suggest improvements.",
        "mindmap": "You are a concept mapper. Use ONLY the retrieved document context. Create a structured mind map with a central topic, branches, and links to key ideas.",
        "study_plan": "You are a study planner. Use ONLY the retrieved document context. Build a practical study plan based on exam date, available hours, difficulty, progress, and weak areas.",
        "comparison": "You are a comparison assistant. Use ONLY the retrieved document context. Compare the requested topics, highlight similarities and differences, and provide takeaways.",
        "general": "You are a helpful AI learning assistant grounded in the uploaded source documents. Answer using retrieved context first, stay accurate, and clearly separate general knowledge from document-grounded knowledge.",
    }

    def get_prompt(self, action: str, context: str = "", question: str = "") -> str:
        base_prompt = self.TEMPLATES.get(action, self.TEMPLATES["general"])

        if not context:
            return (
                f"{base_prompt}\n\n"
                "No document context was available. Respond only with a clear, honest message that says the document context is missing."
            )

        return (
            f"{base_prompt}\n\n"
            "Use ONLY the following document context.\n\n"
            f"<context>\n{context}\n</context>\n\n"
            f"Task: {question}"
        )
