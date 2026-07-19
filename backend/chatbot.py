from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

def ask_ai(messages):
    stream = client.chat.completions.create(
        model="tencent/hy3:free",
        messages=messages,
        stream=True
    )

    full_response = ""

    print("\nAI: ", end="", flush=True)

    for chunk in stream:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            full_response += text

            print(text, end="", flush=True)

    print()

    return full_response