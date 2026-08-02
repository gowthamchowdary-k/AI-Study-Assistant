import re
import time

from memory import (
    get_history,
    add_user_message,
    add_ai_message
)
from prompts.prompt_manager import PromptManager
from providers.provider_factory import get_provider

PROMPT_MANAGER = PromptManager()


def format_math(answer: str) -> str:
    """
    Automatically wraps common LaTeX expressions in $...$
    so KaTeX can render them.
    """

    patterns = [
        r'\\frac\{.*?\}\{.*?\}',
        r'\\sqrt\{.*?\}',
        r'\\sum',
        r'\\alpha',
        r'\\beta',
        r'\\gamma',
        r'\\theta',
        r'\\lambda',
        r'\\sigma',
        r'\\mu',
        r'\\pi',
        r'\\Delta',
        r'\\int',
        r'\\lim',
        r'\\log',
        r'\\sin',
        r'\\cos',
        r'\\tan'
    ]

    for pattern in patterns:

        answer = re.sub(
            fr'(?<!\$)({pattern})(?!\$)',
            r'$\1$',
            answer
        )

    return answer


def build_messages(question, context, action="general", prompt_override=None):
    """
    Builds the message list sent to the LLM.
    """

    history = get_history()[-6:]

    prompt = prompt_override or PROMPT_MANAGER.get_prompt(
        action,
        context=context,
        question=question
    )

    system_prompt = f"""
You are an advanced AI Study Assistant that answers strictly from the retrieved document context.

==========================
Learning Mode
==========================
Action:
{action}

==========================
Retrieved Document Context
==========================
{context}

==========================
Instructions
==========================
{prompt}

==========================
Rules
==========================

1. Treat every retrieved document as an independent source.

2. If multiple documents are retrieved, use information from ALL relevant documents before answering.

3. Never ignore a relevant document simply because another document appears first.

4. When different documents contribute different information, combine them into one coherent answer.

5. Compare information across documents whenever appropriate.

6. If only one document contains the answer, answer only from that document.

7. Never invent facts.

8. If information is missing from the retrieved documents, clearly state:

"The uploaded documents do not contain this information."

Then optionally provide a General Knowledge section.

9. Mention filenames naturally where helpful.

10. Keep answers structured.

11. Prefer retrieved context over model knowledge.

12. Never contradict retrieved context.

13. End long answers with a short summary.

14. VERY IMPORTANT:
Whenever you write mathematical equations,
ALWAYS use LaTeX enclosed in $$...$$.

Example:

$$
Recall = \\frac{{TP}}{{TP+FN}}
$$

Never output raw expressions like

\\frac{{TP}}{{TP+FN}}

without $$ delimiters.
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
    Returns the complete response.
    """

    messages = build_messages(
        question,
        context,
        action=action
    )

    try:

        provider = get_provider()

        answer = provider.generate(messages)

        answer = format_math(answer)

    except RuntimeError as exc:

        raise ValueError(str(exc)) from exc

    add_user_message(question)
    add_ai_message(answer)

    return answer


def ask_ai_stream(question, context, action="general"):
    """
    Streams the response.
    """

    messages = build_messages(
        question,
        context,
        action=action
    )

    try:

        provider = get_provider()

        print("=" * 80)
        print("Model:", provider.model)
        print("Messages:", len(messages))
        print("System Prompt Length:", len(messages[0]["content"]))
        print("=" * 80)

        start = time.time()

        stream = provider.generate_stream(messages)

    except RuntimeError as exc:

        raise ValueError(str(exc)) from exc

    full_response = ""

    for token in stream:

        full_response += token

        yield token

    full_response = format_math(full_response)

    print("=" * 80)
    print("Gemini Response Time:", round(time.time() - start, 2), "seconds")
    print("=" * 80)

    add_user_message(question)
    add_ai_message(full_response)