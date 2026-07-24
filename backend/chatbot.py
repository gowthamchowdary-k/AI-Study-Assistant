import time
from memory import (
    get_history,
    add_user_message,
    add_ai_message
)
from prompts.prompt_manager import PromptManager
from providers.provider_factory import get_provider

PROMPT_MANAGER = PromptManager()


def build_messages(question, context, action="general", prompt_override=None):
    """
    Builds the message list sent to the LLM.
    """

    history = get_history()[-6:]
    prompt = prompt_override or PROMPT_MANAGER.get_prompt(action, context=context, question=question)

    system_prompt = f"""
You are a production-grade AI Learning Platform assistant.

Use document-grounded reasoning as the primary source.

Action: {action}

Document Context:

{context}

Instructions:
{prompt}

Rules:
1. Use the uploaded document as the primary reference.
2. If the answer is not present in the document, clearly mark it as general knowledge.
3. Never invent document facts.
4. Keep the answer structured, educational, and easy to follow.
5. Prefer concise, accurate and clearly cited explanations.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    return messages


def ask_ai(question, context, action="general"):
    """
    Returns the complete response as a string.
    """

    messages = build_messages(question, context, action=action)

    try:
        provider = get_provider()
        answer = provider.generate(messages)
    except RuntimeError as exc:
        raise ValueError(str(exc)) from exc

    add_user_message(question)
    add_ai_message(answer)

    return answer


def ask_ai_stream(question, context, action="general"):
    """
    Streams the response token-by-token.
    """

    messages = build_messages(question, context, action=action)

    try:
        provider = get_provider()

        print("=" * 80)
        print("Model:", provider.model)
        print("Messages:", len(messages))
        print("System Prompt Length:", len(messages[0]["content"]))
        print("=" * 80)

        start = time.time()

        answer = provider.generate(messages)

        print("=" * 80)
        print("Gemini Response Time:", round(time.time() - start, 2), "seconds")
        print("=" * 80)

    except RuntimeError as exc:
        raise ValueError(str(exc)) from exc

    full_response = ""

    for token in stream:
        full_response += token
        yield token

    add_user_message(question)
    add_ai_message(full_response)