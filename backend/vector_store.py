import os
import pickle
import faiss


DATA_FOLDER = "data"

INDEX_FILE = os.path.join(DATA_FOLDER, "faiss.index")
CHUNKS_FILE = os.path.join(DATA_FOLDER, "chunks.pkl")


def save_vector_store(index, chunks):

    os.makedirs(DATA_FOLDER, exist_ok=True)

    faiss.write_index(index, INDEX_FILE)

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)


def vector_store_exists():

    return (
        os.path.exists(INDEX_FILE)
        and
        os.path.exists(CHUNKS_FILE)
    )


def load_vector_store():

    index = faiss.read_index(INDEX_FILE)

    with open(CHUNKS_FILE, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks