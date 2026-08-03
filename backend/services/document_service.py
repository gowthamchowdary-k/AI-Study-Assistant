import os

from core.app_state import app_state
from vector_store import (
    get_user_upload_folder,
    clear_vector_store
)
from services.rag_service import rebuild_vector_database
from utils import clean_filename, allowed_file


def list_documents(user_id):
    """
    Returns all uploaded documents for the user.
    """
    user_upload_folder = get_user_upload_folder(user_id)
    if not os.path.exists(user_upload_folder):
        return []

    files = []
    for file in os.listdir(user_upload_folder):
        if allowed_file(file):
            files.append(file)
            
    return sorted(files)


def delete_document(filename, user_id):
    """
    Deletes a document for the user and rebuilds the vector database.
    """
    filename = clean_filename(filename)
    user_upload_folder = get_user_upload_folder(user_id)
    file_path = os.path.join(user_upload_folder, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError("Document not found.")

    os.remove(file_path)
    clear_vector_store(user_id)

    remaining = list_documents(user_id)
    if remaining:
        rebuild_vector_database(user_id)
    else:
        app_state.user_indices[user_id] = None
        app_state.user_chunks[user_id] = None

    return filename


def document_exists(filename, user_id):
    """
    Returns True if the document exists for the user.
    """
    filename = clean_filename(filename)
    user_upload_folder = get_user_upload_folder(user_id)
    return os.path.exists(os.path.join(user_upload_folder, filename))


def total_documents(user_id):
    """
    Returns number of uploaded documents for the user.
    """
    return len(list_documents(user_id))