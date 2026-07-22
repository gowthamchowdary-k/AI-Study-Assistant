import faiss
import numpy as np


def create_faiss_index(embeddings):
    """
    Creates a FAISS IndexFlatL2 index from embeddings.

    Parameters:
        embeddings (numpy.ndarray): Shape (num_chunks, embedding_dimension)

    Returns:
        faiss.IndexFlatL2
    """

    embeddings = np.asarray(embeddings, dtype="float32")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D array.")

    if len(embeddings) == 0:
        raise ValueError("No embeddings found.")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index