import logging

from chatbot import ask_ai
from search import search_chunks
from formatter.response_formatter import ResponseFormatter
from intent.intent_router import IntentRouter
from prompts.prompt_manager import PromptManager
from context_builder import ContextBuilder

from memory import (
    save_context,
    get_context,
    get_sources
)

from services.rag_service import (
    get_index,
    get_chunks
)

from utils import (
    is_follow_up,
    is_greeting
)

# -------------------------------
# FAISS relevance threshold
# Smaller L2 distance = better match
# -------------------------------
RELEVANCE_THRESHOLD = 1.2
INTENT_ROUTER = IntentRouter()
PROMPT_MANAGER = PromptManager()
FORMATTER = ResponseFormatter()
CONTEXT_BUILDER = ContextBuilder()
LOGGER = logging.getLogger(__name__)


def build_context(results):
    """
    Uses the context builder to assemble a clean, deduplicated prompt context.
    """

    context, sources, pages, chunk_ids = CONTEXT_BUILDER.build(results)
    LOGGER.info("Built prompt context from %s retrieved chunks", len(chunk_ids))
    return context, sources, pages


def estimate_confidence(best_distance, retrieved_count=0, context_length=0):
    """Converts retrieval distance into a bounded confidence score."""

    if best_distance is None:
        return 0.0

    similarity_component = max(0.0, 1.0 - (best_distance / 2.0))
    count_component = min(1.0, retrieved_count / 5.0)
    completeness_component = min(1.0, context_length / 3000.0)
    score = (similarity_component * 0.55) + (count_component * 0.20) + (completeness_component * 0.25)
    return round(min(0.99, score), 2)


def process_chat(question, action_id=None):
    """
    Main chat pipeline.
    """

    question = question.strip()

    if question == "":
        raise ValueError("Question is required.")

    action = action_id or INTENT_ROUTER.classify(question)

    if is_greeting(question):
        return {
            "answer": "Hello! 👋 How can I help you today?",
            "sources": [],
            "chunksRetrieved": 0,
            "action": action,
            "title": "Welcome"
        }

    if is_follow_up(question) and get_context():

        context = get_context()
        sources = get_sources()
        pages = []
        confidence = 0.0

    else:

        index = get_index()
        chunks = get_chunks()

        results = search_chunks(
            question,
            index,
            chunks
        )

        if not results:
            LOGGER.warning("No retrieval results found for question: %s", question)
            answer = "No document context available. Please upload and index a PDF before asking a document-grounded question."
            return {
                "answer": answer,
                "sources": [],
                "chunksRetrieved": 0,
                "action": action,
                "title": action.replace("_", " ").title(),
                "summary": answer,
                "confidence": 0.0,
                "pages": []
            }

        best_distance = results[0]["distance"]
        print("\nBest FAISS Distance:", best_distance)

        LOGGER.info("Using retrieved PDF context for action=%s", action)
        context, sources, pages = build_context(results)
        confidence = estimate_confidence(best_distance, retrieved_count=len(results), context_length=len(context))
        save_context(context, sources)

        if best_distance > RELEVANCE_THRESHOLD:
            LOGGER.warning("Retrieval score %.4f exceeded relevance threshold %.4f; retaining document-grounded context with lower confidence.", best_distance, RELEVANCE_THRESHOLD)
            confidence = min(confidence, 0.35)

    prompt = PROMPT_MANAGER.get_prompt(action, context=context, question=question)
    answer = ask_ai(question, context, action=action)

    structured = FORMATTER.format(
        title=action.replace("_", " ").title(),
        answer=answer,
        sources=sources,
        confidence=confidence,
        pages=pages,
        follow_up_questions=["What would you like to study next?"],
        study_tips=["Review the relevant pages and test the concept with a follow-up question."],
    )

    structured.update({
        "answer": answer,
        "sources": sources,
        "chunksRetrieved": len(sources),
        "action": action,
        "prompt": prompt
    })

    return structured