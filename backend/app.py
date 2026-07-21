from pdf_reader import read_pdf
from splitter import split_text
from embeddings import create_embeddings
from faiss_db import create_faiss_index
from search import search_chunks
from chatbot import ask_ai
from memory import save_context, get_context

from vector_store import (
    save_vector_store,
    load_vector_store,
    vector_store_exists
)

# -----------------------------------
# Follow-up Question Detection
# -----------------------------------

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


# -----------------------------------
# Load Vector Store
# -----------------------------------

if vector_store_exists():

    print("\nLoading existing vector database...\n")

    index, chunks = load_vector_store()

else:

    print("\nCreating vector database...\n")

    pdf_path = "paper2.pdf"

    text = read_pdf(pdf_path)

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    save_vector_store(index, chunks)

    print("\nVector database saved.\n")


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

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ]

    if question.lower() in greetings:

        print("\nAI: Hello! How can I help you today?")
        continue

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