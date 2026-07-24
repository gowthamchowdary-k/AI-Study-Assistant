from embeddings import model


def similarity_from_distance(distance):
    """Convert L2 distance into a 0..1 similarity score."""

    if distance is None:
        return 0.0

    similarity = max(0.0, 1.0 - (float(distance) / 10.0))
    return round(similarity, 4)


def search_chunks(question, index, chunks, k=5):
    """
    Searches the FAISS index and returns the most relevant,
    unique chunks with document metadata and similarity score.
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
            chunk.get("file"),
            chunk.get("page"),
            chunk.get("text")
        )

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk.get("text"),
            "file": chunk.get("file"),
            "page": chunk.get("page"),
            "distance": round(float(distance), 4),
            "similarity": similarity_from_distance(distance),
            "chapter": chunk.get("chapter"),
            "heading": chunk.get("heading"),
            "keywords": chunk.get("keywords", []),
            "summary": chunk.get("summary")
        })

    print("\n========== Search Results ==========")
    for r in results:
        print(
            f"{r['file']} | Page {r['page']} | Distance = {r['distance']} | Similarity = {r['similarity']}"
        )
    print("====================================\n")

    return results