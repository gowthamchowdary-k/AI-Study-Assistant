import os
import traceback

from vector_store import (
    get_upload_folder,
    clear_vector_store
)

from services.rag_service import rebuild_vector_database
from utils import (
    allowed_file,
    clean_filename
)

UPLOAD_FOLDER = get_upload_folder()


def upload_pdf(file):
    """
    Validates and uploads a PDF.
    Automatically rebuilds the vector database.
    """

    if file is None:
        raise ValueError("No file uploaded.")

    if file.filename == "":
        raise ValueError("No file selected.")

    if not allowed_file(file.filename):
        raise ValueError("Only PDF files are allowed.")

    filename = clean_filename(file.filename)

    save_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(save_path):
        raise ValueError(
            f'"{filename}" has already been uploaded.'
        )

    try:
        # Save the PDF
        file.save(save_path)
        print(f"Uploaded: {filename}")

        # Rebuild the vector database
        clear_vector_store()
        rebuild_vector_database()

        print("Vector database rebuilt successfully.")

        return filename

    except Exception as e:

        # Remove the uploaded file if indexing fails
        if os.path.exists(save_path):
            os.remove(save_path)

        print("=" * 60)
        print("UPLOAD FAILED")
        traceback.print_exc()
        print("=" * 60)

        raise Exception(f"Failed to index PDF: {e}")