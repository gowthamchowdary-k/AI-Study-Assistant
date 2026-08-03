import logging
import os

from core.app_state import app_state
from embeddings import create_embeddings
from faiss_db import create_faiss_index
from pdf_reader import read_document
from rag.document_processor import DocumentProcessor
from splitter import split_text
from vector_store import (
    get_user_upload_folder,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)
from utils import ALLOWED_EXTENSIONS

LOGGER = logging.getLogger(__name__)


def build_vector_database(user_id):
    """
    Reads every uploaded document for the user, extracts text, cleans it, chunks it, embeds it,
    and stores the FAISS index and chunk metadata.
    """
    upload_folder = get_user_upload_folder(user_id)
    
    # Get all allowed files in the upload folder
    all_files = []
    for file_name in os.listdir(upload_folder):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            all_files.append(os.path.join(upload_folder, file_name))

    if not all_files:
        print(f"RAG INFO: No documents found to index for user {user_id}.")
        # Reset state cache for user
        app_state.user_indices[user_id] = None
        app_state.user_chunks[user_id] = None
        return

    processor = DocumentProcessor()
    all_pages = []

    for file_path in all_files:
        print(f"\nReading: {os.path.basename(file_path)}")
        try:
            pages = read_document(file_path)
            print(f"Pages/sections extracted: {len(pages)}")
            cleaned_pages = processor.clean_text_pages(pages)
            print(f"Pages after cleaning: {len(cleaned_pages)}")
            all_pages.extend(cleaned_pages)
        except Exception as e:
            print(f"ERROR reading {os.path.basename(file_path)}: {e}")
            continue

    if not all_pages:
        raise Exception("Failed to extract text from any of the uploaded documents.")

    print("\n================================")
    print("TOTAL PAGES:", len(all_pages))
    print("================================")

    chunks = split_text(all_pages)
    LOGGER.info("Chunked %s pages into %s chunks", len(all_pages), len(chunks))

    embeddings = create_embeddings(chunks)
    LOGGER.info("Created %s embeddings", len(embeddings))

    index = create_faiss_index(embeddings)
    LOGGER.info("Built FAISS index with %s entries", index.ntotal)

    save_vector_store(index, chunks, user_id)

    app_state.user_indices[user_id] = index
    app_state.user_chunks[user_id] = chunks

    print("=" * 50)
    print(f"Indexed {len(all_files)} document(s)")
    print(f"Created {len(chunks)} chunks")
    print("=" * 50)


def ensure_vector_database(user_id):
    """
    Loads the vector database if available.
    Otherwise builds it.
    """
    if (
        user_id in app_state.user_indices
        and app_state.user_indices[user_id] is not None
        and user_id in app_state.user_chunks
        and app_state.user_chunks[user_id] is not None
    ):
        return

    if vector_store_exists(user_id):
        print(f"Loading existing vector database for user {user_id}...")
        index, chunks = load_vector_store(user_id)
        app_state.user_indices[user_id] = index
        app_state.user_chunks[user_id] = chunks
    else:
        build_vector_database(user_id)


def get_index(user_id):
    ensure_vector_database(user_id)
    return app_state.user_indices.get(user_id)


def get_chunks(user_id):
    ensure_vector_database(user_id)
    return app_state.user_chunks.get(user_id)


def rebuild_vector_database(user_id):
    """
    Rebuilds the complete vector database.
    Useful after uploading or deleting documents.
    """
    build_vector_database(user_id)