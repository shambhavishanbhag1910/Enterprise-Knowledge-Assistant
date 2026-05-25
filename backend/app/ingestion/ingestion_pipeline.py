import json
from pathlib import Path
from typing import List, Dict, Any

from backend.app.ingestion.document_loader import load_document
from backend.app.ingestion.text_cleaner import clean_text
from backend.app.ingestion.chunker import chunk_text


def save_chunks_to_jsonl(chunks: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save chunks into JSONL file.
    JSONL means one JSON object per line.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def run_ingestion(
    input_folder: str = "data/sample_documents",
    output_path: str = "data/chunks/document_chunks.jsonl"
) -> List[Dict[str, Any]]:
    """
    Full ingestion pipeline:
    1. Read documents
    2. Clean text
    3. Create chunks
    4. Save chunks
    """
    input_path = Path(input_folder)

    if not input_path.exists():
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    supported_extensions = [".txt", ".pdf"]
    all_chunks = []

    for file_path in input_path.iterdir():
        if file_path.suffix.lower() not in supported_extensions:
            print(f"Skipping unsupported file: {file_path.name}")
            continue

        print(f"Processing document: {file_path.name}")

        document = load_document(str(file_path))
        document["text"] = clean_text(document["text"])

        chunks = chunk_text(document)
        all_chunks.extend(chunks)

    save_chunks_to_jsonl(all_chunks, output_path)

    print(f"\nIngestion completed successfully.")
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Chunks saved at: {output_path}")

    return all_chunks


if __name__ == "__main__":
    run_ingestion()