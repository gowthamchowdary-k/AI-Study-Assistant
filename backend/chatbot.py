from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

def ask_ai(question):
    response = client.chat.completions.create(
        model="tencent/hy3:free",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content