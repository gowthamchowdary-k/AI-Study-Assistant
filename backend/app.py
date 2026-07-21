from pdf_reader import read_pdf
from splitter import split_text
from embeddings import create_embeddings
from faiss_db import create_faiss_index
from search import search_chunks
from chatbot import ask_ai
from memory import save_context, get_context

# -----------------------------
# Detect follow-up questions
# -----------------------------
FOLLOW_UP_WORDS = [
    "explain",
    "simple",
    "easy",
    "example",
    "why",
    "how",
    "more",
    "details",
    "summarize",
    "summary",
    "continue",
    "elaborate",
    "again",
    "it",
    "this",
    "that"
]


def is_follow_up(question):
    question = question.lower()

    for word in FOLLOW_UP_WORDS:
        if word in question:
            return True

    return False


# -----------------------------
# Load PDF
# -----------------------------
pdf_path = "paper2.pdf"

text = read_pdf(pdf_path)

chunks = split_text(text)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)

print("=" * 50)
print("📚 AI Study Assistant (Conversational RAG)")
print("=" * 50)

while True:

    question = input("\nYou: ").strip()

    if not question:
        print("Please enter a question.")
        continue

    if question.lower() == "exit":
        print("Goodbye!")
        break

    # ------------------------------------
    # Follow-up question
    # ------------------------------------
    if is_follow_up(question) and get_context():

        print("\nUsing previous context...\n")

        context = get_context()

    else:

        relevant_chunks = search_chunks(
            question,
            index,
            chunks,
            k=3
        )

        print("\n========== RETRIEVED CHUNKS ==========\n")

        for i, chunk in enumerate(relevant_chunks, start=1):
            print(f"Chunk {i}\n")
            print(chunk[:300])
            print("-" * 60)

        context = "\n\n".join(relevant_chunks)

        save_context(context)

    ask_ai(question, context)