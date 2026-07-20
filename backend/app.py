from pdf_reader import read_pdf
from splitter import split_text
from embeddings import create_embeddings
from faiss_db import create_faiss_index
from search import search_chunks
from chatbot import ask_ai

pdf_path = "paper2.pdf"

text = read_pdf(pdf_path)

chunks = split_text(text)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)

print("=" * 50)
print("📚 AI Study Assistant (RAG)")
print("=" * 50)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

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

    ask_ai(question, context)