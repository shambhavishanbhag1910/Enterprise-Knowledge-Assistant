from pathlib import Path
from typing import Dict, Any
from pypdf import PdfReader


def load_txt(file_path: str) -> str:
    """Load text from a TXT file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    pages_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages_text.append(f"\n--- Page {page_number} ---\n{text}")

    return "\n".join(pages_text)


def load_document(file_path: str) -> Dict[str, Any]:
    """
    Load document based on file extension.
    First version supports TXT and PDF.
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".txt":
        text = load_txt(file_path)
    elif extension == ".pdf":
        text = load_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return {
        "document_name": path.name,
        "source_path": str(path),
        "file_type": extension.replace(".", ""),
        "text": text,
    }