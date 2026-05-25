from typing import List, Dict, Any


def chunk_text(
    document: Dict[str, Any],
    chunk_size: int = 180,
    overlap: int = 40
) -> List[Dict[str, Any]]:
    """
    Split document text into overlapping word-based chunks.

    For first version, we are using word-based chunking.
    Later, we can improve this using token-based and heading-based chunking.
    """
    text = document["text"]
    words = text.split()

    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_value = " ".join(chunk_words)

        chunk_id = (
            document["document_name"]
            .replace(".", "_")
            .replace(" ", "_")
            .lower()
            + f"_chunk_{chunk_number:03d}"
        )

        chunks.append(
            {
                "chunk_id": chunk_id,
                "document_name": document["document_name"],
                "source_path": document["source_path"],
                "file_type": document["file_type"],
                "chunk_number": chunk_number,
                "chunk_text": chunk_text_value,
            }
        )

        chunk_number += 1

        # Move forward with overlap
        start += chunk_size - overlap

    return chunks