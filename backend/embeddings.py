from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Creates embeddings for the text inside each chunk.

    Input:
    [
        {
            "text": "...",
            "file": "...",
            "page": 1
        }
    ]

    Output:
        numpy.ndarray (float32)
    """

    if not chunks:
        raise ValueError("No text chunks found to embed.")

    texts = [
        chunk["text"].strip()
        for chunk in chunks
        if chunk.get("text", "").strip()
    ]

    if not texts:
        raise ValueError("All extracted chunks are empty.")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    if embeddings.ndim != 2:
        raise ValueError(
            f"Expected a 2D embedding array, got shape {embeddings.shape}"
        )

    return embeddings