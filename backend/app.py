from chatbot import ask_ai

print("=" * 40)
print("🤖 AI Study Assistant")
print("=" * 40)

question = input("Ask: ")

answer = ask_ai(question)

print("\nAI:")
print(answer)