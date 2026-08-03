import os
import threading
import traceback

from vector_store import get_user_upload_folder
from services.rag_service import rebuild_vector_database
from utils import allowed_file, clean_filename
from database import add_document_record


def upload_document(file, user_id):
    """
    Saves the file to local storage, creates an initial database record as 'Uploaded',
    spawns a background thread to build the vector database asynchronously,
    and returns the filename immediately.
    """
    if file is None:
        raise ValueError("No file uploaded.")

    if file.filename == "":
        raise ValueError("No file selected.")

    if not allowed_file(file.filename):
        raise ValueError(
            "Unsupported file format. Allowed formats: PDF, DOCX, PPTX, TXT, and common Images (PNG, JPG, JPEG, WEBP)."
        )

    filename = clean_filename(file.filename)
    user_upload_folder = get_user_upload_folder(user_id)
    save_path = os.path.join(user_upload_folder, filename)

    # 1. Save the file to writeable folder
    file.save(save_path)
    print(f"Uploaded and saved: {filename} for user {user_id}")

    # 2. Add database tracking record immediately
    add_document_record(user_id, filename, file.filename, "Uploaded")

    # 3. Spawn background thread to index RAG context asynchronously
    def index_worker():
        try:
            print(f"Background indexing thread started for user {user_id}...")
            rebuild_vector_database(user_id)
            print(f"Background indexing completed successfully for user {user_id}.")
        except Exception as err:
            print(f"CRITICAL: Background indexing thread failed for user {user_id}: {err}")
            traceback.print_exc()

    thread = threading.Thread(target=index_worker)
    thread.start()

    return filename