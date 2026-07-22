from pypdf import PdfReader
import os


def read_pdf(file_path):
    """
    Reads a PDF page by page and returns metadata.

    Returns:
    [
        {
            "file": "paper.pdf",
            "page": 1,
            "text": "..."
        },
        ...
    ]
    """

    reader = PdfReader(file_path)

    pages = []

    file_name = os.path.basename(file_path)

    for page_number, page in enumerate(reader.pages, start=1):

        extracted = page.extract_text()

        if extracted and extracted.strip():

            pages.append(
                {
                    "file": file_name,
                    "page": page_number,
                    "text": extracted
                }
            )

    return pages