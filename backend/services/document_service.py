import os
import glob

from core.app_state import app_state

from vector_store import (
    get_upload_folder,
    clear_vector_store
)

from services.rag_service import rebuild_vector_database
from utils import clean_filename


UPLOAD_FOLDER = get_upload_folder()


def list_documents():
    """
    Returns all uploaded PDF documents.
    """

    files = sorted(
        os.path.basename(file)
        for file in glob.glob(
            os.path.join(
                UPLOAD_FOLDER,
                "*.pdf"
            )
        )
    )

    return files


def delete_document(filename):
    """
    Deletes a PDF document and
    rebuilds the vector database.
    """

    filename = clean_filename(filename)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Document not found."
        )

    os.remove(file_path)

    clear_vector_store()

    remaining = glob.glob(
        os.path.join(
            UPLOAD_FOLDER,
            "*.pdf"
        )
    )

    if remaining:

        rebuild_vector_database()

    else:

        app_state.index = None
        app_state.chunks = None

    return filename


def document_exists(filename):
    """
    Returns True if the document exists.
    """

    filename = clean_filename(filename)

    return os.path.exists(
        os.path.join(
            UPLOAD_FOLDER,
            filename
        )
    )


def total_documents():
    """
    Returns number of uploaded PDFs.
    """

    return len(list_documents())