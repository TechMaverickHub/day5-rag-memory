from pathlib import Path
import json
import os

import faiss
import numpy as np

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

import google.generativeai as genai

from memory import (
    add_message,
    get_history,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "indexes" / "pdf.index"

CHUNKS_PATH = BASE_DIR / "indexes" / "chunks.json"

# -----------------------
# Gemini
# -----------------------

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -----------------------
# Embeddings
# -----------------------

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------
# Load FAISS
# -----------------------

index = faiss.read_index(
    str(INDEX_PATH)
)

with open(
    CHUNKS_PATH,
    encoding="utf-8"
) as f:
    chunks = json.load(f)


def retrieve(
    query: str,
    top_k: int = 3,
):
    query_embedding = (
        embedding_model.encode(
            [query]
        )
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = (
        index.search(
            query_embedding,
            top_k
        )
    )

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(
            chunks[idx]
        )

    return retrieved_chunks


def build_prompt(
    question: str,
    retrieved_chunks: list,
):
    context = "\n\n".join(
        retrieved_chunks
    )

    history = get_history()

    return f"""
You are a helpful AI assistant.

Answer ONLY using
the provided document context.

If the answer is not present
in the context, say:

"I could not find that information in the document."

Conversation History:
{history}

Document Context:
{context}

Question:
{question}
"""


def ask_rag(
    question: str,
):
    retrieved_chunks = retrieve(
        question
    )

    prompt = build_prompt(
        question,
        retrieved_chunks
    )

    response = llm.generate_content(
        prompt
    )

    answer = response.text

    add_message(
        "User",
        question
    )

    add_message(
        "Assistant",
        answer
    )

    return {
        "answer": answer,
        "chunks": retrieved_chunks,
    }


if __name__ == "__main__":

    print(
        "\nPDF RAG Assistant Ready"
    )

    while True:

        question = input(
            "\nAsk: "
        )

        if question.lower() == "exit":
            break

        result = ask_rag(
            question
        )

        print("\n")
        print(result["answer"])