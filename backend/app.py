from chatbot import ask_ai

messages = [
    {
        "role": "system",
        "content": (
            "You are an AI Study Assistant. "
            "Always respond in English "
            "Give clear, accurate and concise answers."
        )
    }
]

print("=" * 40)
print("🤖 AI Study Assistant")
print("=" * 40)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("\n👋 Thank you for using AI Study Assistant!")
        break

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    try:
        answer = ask_ai(messages)

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


    except Exception as e:
        print("\nAI:")
        print("❌ Sorry, I couldn't contact the AI service.")
        print(f"Error: {e}")