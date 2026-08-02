from embeddings import model
from collections import defaultdict 

def similarity_from_distance(distance):
    """Convert L2 distance into a 0..1 similarity score."""

    if distance is None:
        return 0.0

    similarity = max(0.0, 1.0 - (float(distance) / 10.0))
    return round(similarity, 4)


def search_chunks(question, index, chunks,
                  retrieve_k=30,
                  max_chunks_per_document=3):
    """
    Commercial-grade retrieval.

    1. Retrieve many chunks.
    2. Group by PDF.
    3. Keep best chunks from EACH PDF.
    4. Return balanced multi-document context.
    """

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        question_embedding,
        retrieve_k
    )

    grouped = defaultdict(list)

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

        if key in seen:
            continue

        seen.add(key)

        grouped[chunk["file"]].append({

            "chunk_id": chunk.get("chunk_id"),

            "text": chunk["text"],

            "file": chunk["file"],

            "page": chunk["page"],

            "distance": round(float(distance),4),

            "similarity": similarity_from_distance(distance),

            "chapter": chunk.get("chapter"),

            "heading": chunk.get("heading"),

            "keywords": chunk.get("keywords", []),

            "summary": chunk.get("summary")
        })


    results = []

    print("\n========== MULTI DOCUMENT SEARCH ==========")

    for document in grouped:

    # Sort chunks inside each document
        grouped[document].sort(
            key=lambda x: x["distance"]
        )

    # Keep only best chunks from that PDF
        selected = grouped[document][:max_chunks_per_document]

        results.extend(selected)

        print(f"{document} -> {len(selected)} chunks")

# Finally sort all selected chunks
    results.sort(
        key=lambda x: x["distance"]
    )

    print("===========================================")

    return results