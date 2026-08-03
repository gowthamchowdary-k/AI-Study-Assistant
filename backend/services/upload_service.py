import os
import traceback

from vector_store import (
    get_user_upload_folder,
    clear_vector_store
)
from services.rag_service import rebuild_vector_database
from utils import (
    allowed_file,
    clean_filename
)


def upload_document(file, user_id):
    """
    Validates and uploads a study material (PDF, DOCX, PPTX, TXT, Images).
    Automatically rebuilds the vector database for the user.
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

    try:
        # Save the new document (overwriting existing file with the same name if it exists)
        file.save(save_path)
        print(f"Uploaded: {filename} for user {user_id}")

        # Clear old vector database and rebuild it incorporating all current documents
        clear_vector_store(user_id)
        rebuild_vector_database(user_id)
        print(f"Vector database rebuilt successfully for user {user_id}.")

        return filename

    except Exception as e:
        # Remove the uploaded file if indexing fails
        if os.path.exists(save_path):
            os.remove(save_path)

        print("=" * 60)
        print(f"UPLOAD FAILED FOR USER {user_id}")
        traceback.print_exc()
        print("=" * 60)

        raise Exception(f"Failed to process and index document: {e}")