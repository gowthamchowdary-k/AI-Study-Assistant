import glob
import logging
import os

from core.app_state import app_state
from embeddings import create_embeddings
from faiss_db import create_faiss_index
from pdf_reader import read_pdf
from rag.document_processor import DocumentProcessor
from search import search_chunks
from splitter import split_text
from vector_store import (
    get_upload_folder,
    load_vector_store,
    save_vector_store,
    vector_store_exists,
)

LOGGER = logging.getLogger(__name__)
UPLOAD_FOLDER = get_upload_folder()


def build_vector_database():
    """
    Reads every uploaded PDF, extracts text, cleans it, chunks it, embeds it,
    and stores the FAISS index and chunk metadata.
    """

    pdf_files = glob.glob(os.path.join(UPLOAD_FOLDER, "*.pdf"))

    if not pdf_files:
        raise Exception("No PDF files found.")

    processor = DocumentProcessor()
    all_pages = []

    for pdf in pdf_files:
        print(f"Reading {os.path.basename(pdf)}")
        pages = read_pdf(pdf)
        cleaned_pages = processor.clean_text_pages(pages)
        all_pages.extend(cleaned_pages)

    chunks = split_text(all_pages)
    LOGGER.info("Chunked %s pages into %s chunks", len(all_pages), len(chunks))

    embeddings = create_embeddings(chunks)
    LOGGER.info("Created %s embeddings", len(embeddings))

    index = create_faiss_index(embeddings)
    LOGGER.info("Built FAISS index with %s entries", index.ntotal)

    save_vector_store(index, chunks)

    app_state.index = index
    app_state.chunks = chunks

    print("=" * 50)
    print(f"Indexed {len(pdf_files)} PDF(s)")
    print(f"Created {len(chunks)} chunks")
    print("=" * 50)


def ensure_vector_database():
    """
    Loads the vector database if available.
    Otherwise builds it.
    """

    if (
        app_state.index is not None
        and
        app_state.chunks is not None
    ):
        return

    if vector_store_exists():

        print("Loading existing vector database...")

        index, chunks = load_vector_store()

        app_state.index = index
        app_state.chunks = chunks

    else:

        build_vector_database()


def get_index():
    ensure_vector_database()
    return app_state.index


def get_chunks():
    ensure_vector_database()
    return app_state.chunks


def rebuild_vector_database():
    """
    Rebuilds the complete vector database.
    Useful after uploading or deleting PDFs.
    """

    build_vector_database()