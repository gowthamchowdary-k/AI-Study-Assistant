import numpy as np

class SimpleVectorIndex:
    """
    A pure Python + NumPy alternative to FAISS IndexFlatL2.
    Removes heavy binary dependencies for serverless deployments.
    """
    def __init__(self, dimension=None):
        self.dimension = dimension
        self.vectors = None

    def add(self, vectors):
        vectors = np.asarray(vectors, dtype="float32")
        if self.vectors is None:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
        self.dimension = self.vectors.shape[1]

    @property
    def ntotal(self):
        return len(self.vectors) if self.vectors is not None else 0

    def search(self, query_vector, k):
        """
        Calculates L2 distance between the query and indexed vectors.
        """
        query_vector = np.asarray(query_vector, dtype="float32")
        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        if self.vectors is None or len(self.vectors) == 0:
            return np.array([[]], dtype="float32"), np.array([[]], dtype="int64")

        # L2 Distance calculation: sum of squared differences
        diff = self.vectors - query_vector
        dist_sq = np.sum(diff ** 2, axis=1)

        # Sort indices by distance (ascending)
        k = min(k, len(dist_sq))
        top_k_indices = np.argsort(dist_sq)[:k]
        top_k_distances = dist_sq[top_k_indices]

        # Return distances and indices formatted exactly like FAISS output
        return np.array([top_k_distances], dtype="float32"), np.array([top_k_indices], dtype="int64")


def create_faiss_index(embeddings):
    """
    Creates a SimpleVectorIndex from embeddings.
    """
    embeddings = np.asarray(embeddings, dtype="float32")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D array.")

    if len(embeddings) == 0:
        raise ValueError("No embeddings found.")

    index = SimpleVectorIndex()
    index.add(embeddings)
    return index