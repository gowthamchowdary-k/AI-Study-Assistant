from embeddings import model
import numpy as np


def search_chunks(question, index, chunks, k=3):

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = index.search(question_embedding, k)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results