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


def get_user_upload_folder(user_id):
    """
    Returns the user-specific upload directory.
    """
    folder = os.path.join(BASE_DIR, "uploads", str(user_id))
    os.makedirs(folder, exist_ok=True)
    return folder


def get_user_data_folder(user_id):
    """
    Returns the user-specific data directory.
    """
    folder = os.path.join(BASE_DIR, "data", str(user_id))
    os.makedirs(folder, exist_ok=True)
    return folder


def get_user_index_file(user_id):
    return os.path.join(get_user_data_folder(user_id), "faiss.index")


def get_user_chunks_file(user_id):
    return os.path.join(get_user_data_folder(user_id), "chunks.pkl")


def save_vector_store(index, chunks, user_id):
    """
    Saves the FAISS index and chunk metadata for the user.
    """
    faiss.write_index(index, get_user_index_file(user_id))

    with open(get_user_chunks_file(user_id), "wb") as file:
        pickle.dump(chunks, file)


def vector_store_exists(user_id):
    """
    Checks whether a saved vector database exists for the user.
    """
    return (
        os.path.exists(get_user_index_file(user_id))
        and
        os.path.exists(get_user_chunks_file(user_id))
    )


def load_vector_store(user_id):
    """
    Loads the FAISS index and chunk metadata for the user.
    """
    if not vector_store_exists(user_id):
        return None, None

    index = faiss.read_index(get_user_index_file(user_id))

    with open(get_user_chunks_file(user_id), "rb") as file:
        chunks = pickle.load(file)

    return index, chunks


def get_upload_folder():
    """
    Deprecated: use get_user_upload_folder instead.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    return UPLOAD_FOLDER


def clear_vector_store(user_id):
    """
    Deletes the user's saved vector database files.
    """
    idx_path = get_user_index_file(user_id)
    chk_path = get_user_chunks_file(user_id)
    if os.path.exists(idx_path):
        os.remove(idx_path)
    if os.path.exists(chk_path):
        os.remove(chk_path)