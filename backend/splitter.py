from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages):
    """
    Splits every page into chunks while preserving
    filename, page number, and a stable chunk identifier.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for page in pages:
        split_chunks = splitter.split_text(page["text"])

        for order, chunk in enumerate(split_chunks, start=1):
            chunk_id = f"{page['file']}::p{page['page']}::c{order}"

            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk,
                "file": page["file"],
                "page": page["page"],
                "chapter": page.get("chapter"),
                "heading": page.get("heading"),
                "keywords": page.get("keywords", []),
                "summary": page.get("summary"),
                "similarity": 0.0,
            })

    return chunks