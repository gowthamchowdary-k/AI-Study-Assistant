import os
import glob
from search import search_chunks
from memory import (
    save_context,
    get_context,
    get_sources
)

from core.app_state import app_state

from pdf_reader import read_pdf
from splitter import split_text
from embeddings import create_embeddings
from faiss_db import create_faiss_index

from vector_store import (
    save_vector_store,
    load_vector_store,
    vector_store_exists,
    get_upload_folder
)


UPLOAD_FOLDER = get_upload_folder()


def build_vector_database():
    """
    Reads every uploaded PDF,
    creates embeddings,
    builds the FAISS index,
    and stores everything.
    """

    pdf_files = glob.glob(
        os.path.join(
            UPLOAD_FOLDER,
            "*.pdf"
        )
    )

    if not pdf_files:
        raise Exception("No PDF files found.")

    all_pages = []

    for pdf in pdf_files:

        print(f"Reading {os.path.basename(pdf)}")

        pages = read_pdf(pdf)

        all_pages.extend(pages)

    chunks = split_text(all_pages)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

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