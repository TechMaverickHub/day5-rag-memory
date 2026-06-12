from pathlib import Path
import json

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "indexes"

PDF_PATH = DATA_DIR / "sample.pdf"

INDEX_DIR.mkdir(exist_ok=True)


def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF."""

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
):
    """Create overlapping chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def create_embeddings(chunks):
    """Generate embeddings."""

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        chunks,
        show_progress_bar=True,
    )

    return np.array(
        embeddings
    ).astype("float32")


def build_faiss_index(embeddings):
    """Build FAISS index."""

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def main():
    print("Loading PDF...")

    text = extract_text(PDF_PATH)

    print(
        f"Extracted {len(text)} characters"
    )

    chunks = chunk_text(text)

    print(
        f"Created {len(chunks)} chunks"
    )

    print("Generating embeddings...")

    embeddings = create_embeddings(
        chunks
    )

    print("Building FAISS index...")

    index = build_faiss_index(
        embeddings
    )

    faiss.write_index(
        index,
        str(INDEX_DIR / "pdf.index")
    )

    with open(
        INDEX_DIR / "chunks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print("\nDone!")
    print(
        f"Index saved: {INDEX_DIR / 'pdf.index'}"
    )
    print(
        f"Chunks saved: {INDEX_DIR / 'chunks.json'}"
    )


if __name__ == "__main__":
    main()