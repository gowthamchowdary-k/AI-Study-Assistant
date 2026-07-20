from config import client


MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


def ask_ai(question, context):

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Study Assistant.\n\n"
                "Answer the user's question ONLY using the document below.\n\n"
                "If the answer exists, explain it clearly.\n"
                "If the answer does not exist, reply exactly:\n"
                "'I couldn't find that information in the document.'\n\n"
                f"DOCUMENT:\n\n{context}"
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

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

    return full_response