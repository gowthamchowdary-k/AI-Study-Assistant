from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages):
    """
    Splits every page into chunks while preserving
    filename and page number.

    Input:
    [
        {
            "file": "AI.pdf",
            "page": 1,
            "text": "..."
        }
    ]

    Output:
    [
        {
            "text": "...",
            "file": "AI.pdf",
            "page": 1
        },
        ...
    ]
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for page in pages:

        split_chunks = splitter.split_text(page["text"])

        for chunk in split_chunks:

            chunks.append({
                "text": chunk,
                "file": page["file"],
                "page": page["page"]
            })

    return chunks