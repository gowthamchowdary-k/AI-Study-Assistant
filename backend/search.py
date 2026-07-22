from embeddings import model
import numpy as np


def search_chunks(question, index, chunks, k=5):
    """
    Searches the FAISS index and returns the most relevant,
    unique chunks with document metadata.
    """

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(question_embedding, k)

    results = []
    seen = set()

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        chunk = chunks[idx]

        key = (
            chunk["file"],
            chunk["page"],
            chunk["text"]
        )

        # Skip duplicate chunks
        if key in seen:
            continue

        seen.add(key)

        results.append({
            "text": chunk["text"],
            "file": chunk["file"],
            "page": chunk["page"],
            "distance": round(float(distance), 4)
        })

    return results