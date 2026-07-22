from chatbot import ask_ai
from search import search_chunks

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


def build_context(results):
    """
    Builds the document context sent to the LLM.
    """

    context_parts = []
    sources = []
    seen = set()

    for item in results:

        context_parts.append(
            f"""
================================================

Document : {item['file']}

Page : {item['page']}

Content:

{item['text']}

================================================
"""
        )

        key = (
            item["file"],
            item["page"]
        )

        if key not in seen:

            seen.add(key)

            # Store only filename in SQLite
            sources.append(item["file"])

    context = "\n".join(context_parts)

    return context, sources


def process_chat(question):
    """
    Main chat pipeline.
    """

    question = question.strip()

    if question == "":
        raise ValueError("Question is required.")

    # Greeting

    if is_greeting(question):

        return {
            "answer": "Hello! 👋 How can I help you today?",
            "sources": [],
            "chunksRetrieved": 0
        }

    # Follow-up

    if is_follow_up(question) and get_context():

        context = get_context()
        sources = get_sources()

    else:

        index = get_index()
        chunks = get_chunks()

        results = search_chunks(
            question,
            index,
            chunks
        )

        if not results:

            return {
                "answer": "I couldn't find relevant information in the uploaded documents.",
                "sources": [],
                "chunksRetrieved": 0
            }

        context, sources = build_context(results)

        save_context(
            context,
            sources
        )

    answer = ask_ai(
        question,
        context
    )

    return {
        "answer": answer,
        "sources": sources,
        "chunksRetrieved": len(sources)
    }