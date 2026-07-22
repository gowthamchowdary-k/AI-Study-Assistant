import os
import pickle
import faiss


# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data folder
DATA_FOLDER = os.path.join(BASE_DIR, "data")

# Upload folder (stores uploaded PDFs)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Vector database files
INDEX_FILE = os.path.join(DATA_FOLDER, "faiss.index")
CHUNKS_FILE = os.path.join(DATA_FOLDER, "chunks.pkl")


def initialize_folders():
    """
    Creates required folders if they don't exist.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_vector_store(index, chunks):
    """
    Saves the FAISS index and chunk metadata.
    """

    initialize_folders()

    faiss.write_index(index, INDEX_FILE)

    with open(CHUNKS_FILE, "wb") as file:
        pickle.dump(chunks, file)


def vector_store_exists():
    """
    Checks whether a saved vector database exists.
    """

    return (
        os.path.exists(INDEX_FILE)
        and
        os.path.exists(CHUNKS_FILE)
    )


def load_vector_store():
    """
    Loads the FAISS index and chunk metadata.
    """

    if not vector_store_exists():
        return None, None

    index = faiss.read_index(INDEX_FILE)

    with open(CHUNKS_FILE, "rb") as file:
        chunks = pickle.load(file)

    return index, chunks


def get_upload_folder():
    """
    Returns the upload directory path.
    """

    initialize_folders()

    return UPLOAD_FOLDER


def clear_vector_store():
    """
    Deletes the saved vector database.
    Useful when rebuilding from uploaded PDFs.
    """

    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

    if os.path.exists(CHUNKS_FILE):
        os.remove(CHUNKS_FILE)