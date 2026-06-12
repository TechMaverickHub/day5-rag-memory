# Conversational PDF RAG Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to chat with PDF documents using semantic search, conversational memory, and Gemini.

Unlike a basic RAG chatbot, this application remembers previous interactions and supports follow-up questions, creating a more natural conversational experience.

This project is part of my AI Engineering learning journey, progressing from embeddings and vector search to building production-style AI assistants.

---

## Demo

### User

```text
What is Django ORM?
```

### Assistant

```text
Django ORM is a database abstraction layer that allows developers to interact with databases using Python objects.
```

### User

```text
How do I optimize it?
```

### Assistant

```text
You can optimize Django ORM using select_related and prefetch_related to reduce database queries and avoid N+1 query issues.
```

Notice that the assistant understands that **"it" refers to Django ORM** by using conversation memory.

---

## Architecture

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Store
 ↓
Retriever
 ↓
Conversation Memory
 ↓
Prompt Construction
 ↓
Gemini
 ↓
Answer
```

---

## Features

- PDF text extraction
- Semantic search using embeddings
- FAISS vector retrieval
- Conversational memory
- Multi-turn interactions
- Context-aware follow-up questions
- Gemini integration
- Streamlit chat interface
- UV dependency management

---

## Tech Stack

### AI / GenAI

- Sentence Transformers
- Gemini 2.5 Flash
- FAISS

### Backend

- Python 3.12+
- UV

### Document Processing

- PyPDF

### Frontend

- Streamlit

---

## Project Structure

```text
day4-rag-memory/
│
├── data/
│   └── sample.pdf
│
├── indexes/
│   ├── pdf.index
│   └── chunks.json
│
├── src/
│   ├── ingest.py
│   ├── memory.py
│   ├── rag.py
│   └── streamlit_app.py
│
├── screenshots/
│
├── .env
├── README.md
├── pyproject.toml
└── uv.lock
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd day4-rag-memory
```

Install dependencies:

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Build Vector Index

Extract text from PDF, create chunks, generate embeddings, and build the FAISS index:

```bash
uv run src/ingest.py
```

Expected Output:

```text
Loading PDF...

Extracted 12450 characters

Created 31 chunks

Generating embeddings...

Building FAISS index...

Done!
```

---

## Run CLI Version

```bash
uv run src/rag.py
```

Example:

```text
Ask:
What is Django ORM?

Ask:
How do I optimize it?
```

---

## Run Streamlit Chat UI

```bash
uv run streamlit run src/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## How It Works

### Step 1: Extract Text

PDF content is extracted using PyPDF.

```python
reader = PdfReader(pdf_path)
```

---

### Step 2: Chunk Documents

Large documents are split into manageable chunks.

```text
Chunk 1
Django ORM Optimization...
```

```text
Chunk 2
Database Indexing...
```

```text
Chunk 3
Caching Strategies...
```

Chunking improves retrieval quality.

---

### Step 3: Generate Embeddings

Each chunk is converted into a vector representation.

```python
embeddings = model.encode(chunks)
```

---

### Step 4: Store in FAISS

Embeddings are stored inside a vector database.

```python
index = faiss.IndexFlatL2(dimension)
```

---

### Step 5: Retrieve Relevant Context

When a user asks a question:

```text
How can I optimize ORM queries?
```

The question is embedded and matched against stored vectors.

```python
distances, indices = index.search(
    query_embedding,
    top_k
)
```

---

### Step 6: Add Conversation History

Previous messages are included in the prompt.

```text
Conversation History
+
Document Context
+
Question
```

This allows the assistant to understand follow-up questions.

---

### Step 7: Generate Grounded Answers

Gemini receives:

```text
Conversation History
+
Retrieved Context
+
User Question
```

and generates a grounded response.

---

## Why Conversation Memory?

### Basic RAG

```text
Question
 ↓
Retrieve
 ↓
Answer
```

Problem:

```text
User:
What is Django ORM?

User:
How do I optimize it?

❌ "it" is ambiguous
```

---

### Memory-Enhanced RAG

```text
Question
 ↓
Retrieve
 ↓
Conversation History
 ↓
Answer
```

Result:

```text
User:
What is Django ORM?

User:
How do I optimize it?

✅ Understands "it" refers to Django ORM
```

---

## Example Conversation

### User

```text
What is database indexing?
```

### Assistant

```text
Database indexing improves query performance by reducing the amount of data scanned.
```

### User

```text
When should I use it?
```

### Assistant

```text
According to the document, indexing should be used on frequently queried columns to improve performance.
```

---

## Interview Questions

### What is RAG?

Retrieval-Augmented Generation is a technique where relevant information is retrieved from external knowledge sources before generating responses.

---

### Why use RAG instead of fine-tuning?

RAG enables dynamic knowledge updates without retraining the model.

---

### What are the main components of a RAG system?

- Document Loader
- Chunking
- Embeddings
- Vector Store
- Retriever
- LLM

---

### What is conversational memory?

A mechanism that stores previous interactions and provides context for future responses.

---

### Why is memory important?

Memory enables follow-up questions and more natural conversations.

---

### How would you scale memory in production?

Options include:

- Redis
- PostgreSQL
- MongoDB
- Vector Databases

instead of in-memory storage.

---

### How can hallucinations be reduced?

- Better chunking
- Improved retrieval
- Grounded prompts
- Memory-aware context
- High-quality embeddings

---

## Learning Journey

### Day 1

- Embeddings
- Semantic Search

### Day 2

- FAISS
- Vector Search

### Day 3

- PDF Processing
- Chunking
- Retrieval

### Day 4

- RAG
- Gemini Integration
- Conversation Memory
- Multi-turn AI Assistants

---

## Future Improvements

- Multi-PDF Support
- Persistent Memory
- Redis Memory Store
- FastAPI Backend
- Docker Deployment
- Authentication
- Qdrant Integration
- Hybrid Search
- Conversation Summarization
- Production Monitoring

---

## Learning Roadmap

- [x] Embeddings
- [x] Semantic Search
- [x] FAISS
- [x] PDF Processing
- [x] Chunking
- [x] Retrieval
- [x] RAG Pipeline
- [x] Conversation Memory
- [ ] FastAPI API
- [ ] Docker Deployment
- [ ] Production AI System

---

## Author

**Abhiroop Bhattacharyya**

Backend Engineer → AI Engineer

### Skills

- Python
- Django
- FastAPI
- Generative AI
- RAG
- FAISS
- Vector Databases
- AI Applications

---

## Connect

Currently building AI Engineering projects in public while transitioning from Backend Development to Generative AI Engineering.

⭐ If you found this project useful, consider giving it a star.