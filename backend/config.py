import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("API Key Loaded:", OPENROUTER_API_KEY is not None)

if OPENROUTER_API_KEY:
    print("Starts with:", OPENROUTER_API_KEY[:10])
else:
    print("API Key NOT FOUND")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)