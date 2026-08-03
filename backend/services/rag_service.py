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
    and stores the vector index and chunk metadata.
    Updates the database with document processing status (Indexing, Ready, Failed).
    """
    from database import get_user_documents, update_document_status

    upload_folder = get_user_upload_folder(user_id)
    
    # 1. Fetch all documents currently tracked in the database for the user
    db_docs = get_user_documents(user_id)
    
    # 2. Map existing documents to list of files to process
    all_files = []
    for doc in db_docs:
        file_path = os.path.join(upload_folder, doc["filename"])
        if os.path.exists(file_path):
            all_files.append(file_path)
            # Update status of any "Uploaded", "Indexing", or "Failed" documents to "Indexing"
            if doc["status"] in ["Uploaded", "Failed", "Indexing"]:
                update_document_status(user_id, doc["filename"], "Indexing")

    if not all_files:
        print(f"RAG INFO: No documents found to index for user {user_id}.")
        # Reset state cache for user
        app_state.user_indices[user_id] = None
        app_state.user_chunks[user_id] = None
        return

    processor = DocumentProcessor()
    all_pages = []
    failed_files = {}

    for file_path in all_files:
        filename = os.path.basename(file_path)
        print(f"\nReading: {filename}")
        try:
            pages = read_document(file_path)
            print(f"Pages/sections extracted: {len(pages)}")
            if not pages:
                raise Exception("No text content could be extracted from this file.")
            cleaned_pages = processor.clean_text_pages(pages)
            print(f"Pages after cleaning: {len(cleaned_pages)}")
            all_pages.extend(cleaned_pages)
        except Exception as e:
            print(f"ERROR reading {filename}: {e}")
            failed_files[filename] = str(e)
            update_document_status(user_id, filename, "Failed", str(e))
            continue

    try:
        if not all_pages:
            raise Exception("No readable text found in any of the uploaded documents.")

        print("\n================================")
        print("TOTAL PAGES:", len(all_pages))
        print("================================")

        chunks = split_text(all_pages)
        LOGGER.info("Chunked %s pages into %s chunks", len(all_pages), len(chunks))

        embeddings = create_embeddings(chunks)
        LOGGER.info("Created %s embeddings", len(embeddings))

        index = create_faiss_index(embeddings)
        LOGGER.info("Built vector index with %s entries", index.ntotal)

        save_vector_store(index, chunks, user_id)

        app_state.user_indices[user_id] = index
        app_state.user_chunks[user_id] = chunks

        # Mark all successfully indexed documents as Ready
        for file_path in all_files:
            filename = os.path.basename(file_path)
            if filename not in failed_files:
                update_document_status(user_id, filename, "Ready")

        print("=" * 50)
        print(f"Indexed {len(all_files) - len(failed_files)} document(s)")
        print(f"Created {len(chunks)} chunks")
        print("=" * 50)

    except Exception as build_err:
        print(f"RAG BUILD CRITICAL ERROR for user {user_id}: {build_err}")
        # Mark all files that were currently "Indexing" as Failed
        for file_path in all_files:
            filename = os.path.basename(file_path)
            if filename not in failed_files:
                update_document_status(user_id, filename, "Failed", f"Index build failed: {build_err}")
        raise build_err


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