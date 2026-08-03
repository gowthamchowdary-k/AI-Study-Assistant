import os
import threading
import traceback

from core.app_state import app_state
from vector_store import get_user_upload_folder, clear_vector_store
from services.rag_service import rebuild_vector_database
from utils import clean_filename
from database import get_user_documents, delete_document_record


def list_documents(user_id):
    """
    Returns all tracked documents for the user from the database.
    """
    return get_user_documents(user_id)


def delete_document(filename, user_id):
    """
    Deletes a document record, removes its physical file, and triggers background index rebuild.
    """
    filename = clean_filename(filename)
    user_upload_folder = get_user_upload_folder(user_id)
    file_path = os.path.join(user_upload_folder, filename)

    # 1. Delete database record
    delete_document_record(user_id, filename)

    # 2. Remove physical file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # 3. Clear RAM cache state and trigger index update in a background thread
    clear_vector_store(user_id)
    
    def delete_worker():
        try:
            # Rebuild index from remaining documents (if any)
            remaining = list_documents(user_id)
            if remaining:
                rebuild_vector_database(user_id)
            else:
                app_state.user_indices[user_id] = None
                app_state.user_chunks[user_id] = None
        except Exception as e:
            print(f"Background indexing thread failed after document delete: {e}")
            traceback.print_exc()

    thread = threading.Thread(target=delete_worker)
    thread.start()

    return filename


def document_exists(filename, user_id):
    """
    Returns True if the document is registered in the database for the user.
    """
    filename = clean_filename(filename)
    docs = get_user_documents(user_id)
    return any(doc["filename"] == filename for doc in docs)


def total_documents(user_id):
    """
    Returns the total number of documents for the user.
    """
    return len(list_documents(user_id))