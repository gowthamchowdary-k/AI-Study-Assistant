from config import client
from memory import (
    get_history,
    add_user_message,
    add_ai_message
)

MODEL = "openrouter/free"


def build_messages(question, context):
    """
    Builds the message list sent to the LLM.
    """

    history = get_history()[-6:]

    system_prompt = f"""
You are an intelligent AI Study Assistant.

Your job is to help students understand concepts clearly, accurately, and naturally.

==========================================================
PRIMARY SOURCE
==========================================================

The uploaded document is your PRIMARY source of information.

Document Context:

{context}

==========================================================
RULES
==========================================================

1. Always use the uploaded document as the primary reference.

2. If the answer exists in the document:
   - Answer using the document.
   - Explain it in simple language.

3. If the user asks:
   - Explain
   - Why
   - How
   - Example
   - Analogy
   - Real-world application
   - Advantages
   - Disadvantages
   - Interview questions

   You may use your own general knowledge to improve the explanation,
   but NEVER contradict the document.

4. If only part of the answer exists in the document:
   - First explain what the document says.
   - Then clearly mention:
     "Additional explanation based on general knowledge:"
   - Continue the explanation.

5. If the answer is completely unrelated to the uploaded document:

   Reply exactly:

   "This information is not available in the uploaded document. However, here's a general explanation."

   Then answer using your general knowledge.

6. Never invent facts about the uploaded document.

7. Never say information exists in the document if it doesn't.

==========================================================
HOW TO EXPLAIN
==========================================================

Whenever possible, structure answers like this:

Definition

Explanation

How it works

Example

Analogy (if helpful)

Applications

Advantages

Disadvantages

Summary

==========================================================
FOR PROGRAMMING OR TECHNICAL QUESTIONS
==========================================================

If the topic is technical (Java, Python, AI, ML, DBMS, OS, CN, Docker, Kubernetes, Cloud, etc.) explain:

• Definition
• Working
• Architecture
• Step-by-step process
• Code example (if applicable)
• Real-world example
• Best practices
• Common mistakes

==========================================================
STYLE
==========================================================

Always:

• Use simple English.
• Use headings.
• Use bullet points.
• Keep answers educational.
• Be friendly like a teacher.
• Answer follow-up questions naturally.

Never refuse to explain something simply because the document only contains a short definition.

Always help the student understand the concept deeply.
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


def ask_ai(question, context):
    """
    Returns the complete response as a string.
    """

    messages = build_messages(question, context)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    add_user_message(question)
    add_ai_message(answer)

    return answer


def ask_ai_stream(question, context):
    """
    Streams the response token-by-token.
    """

    messages = build_messages(question, context)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    full_response = ""

    for chunk in stream:

        if (
            chunk.choices
            and chunk.choices[0].delta
            and chunk.choices[0].delta.content
        ):

            token = chunk.choices[0].delta.content

            full_response += token

            yield token

    add_user_message(question)
    add_ai_message(full_response)