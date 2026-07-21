from config import client
from memory import (
    get_history,
    add_user_message,
    add_ai_message
)

MODEL = "poolside/laguna-xs-2.1:free"


def ask_ai(question, context):

    # Get previous conversation
    history = get_history()

    # Build messages
    messages = [
        {
            "role": "system",
            "content": f"""
You are an AI Study Assistant.

Use the document below as your primary source of information.

Instructions:
- Answer based on the document.
- Explain concepts in simple, easy-to-understand language.
- If the user asks for an explanation, summary, analogy, or example, you may create a simple educational example based on the document.
- Do NOT invent facts that contradict the document.
- If the answer is genuinely not available in the document, reply exactly:
"I couldn't find that information in the document."

DOCUMENT:

{context}
"""
        }
    ]

    # Add previous conversation
    messages.extend(history)

    # Add current user question
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Call the LLM
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    full_response = ""

    print("\nAI: ", end="", flush=True)

    for chunk in stream:

        if (
            chunk.choices
            and chunk.choices[0].delta
            and chunk.choices[0].delta.content
        ):
            text = chunk.choices[0].delta.content
            full_response += text
            print(text, end="", flush=True)

    print()

    # Save conversation history
    add_user_message(question)
    add_ai_message(full_response)

    return full_response