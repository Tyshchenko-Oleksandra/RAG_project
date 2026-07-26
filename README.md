# 📚 University Notes RAG

University Notes RAG is a Retrieval-Augmented Generation application that helps students ask questions based on their university notes.

The system reads lecture materials from PDF and PPTX files, converts them into embeddings, stores them in a vector database, and answers questions using only the retrieved context from the uploaded notes.

---

## ✨ Features

- 📄 PDF document ingestion
- 🖼️ PPTX text extraction support
- 🧠 OpenAI embeddings
- 🔎 Semantic search with ChromaDB
- 📚 Subject-based filtering
- 💬 Question answering with source-aware responses
- 🌐 FastAPI backend
- 🎛️ Streamlit frontend
- 📌 Source labels with file names and page numbers
- 🧱 Clean backend structure with services, routes, schemas, and config

---

## 🧱 Tech Stack

- Python
- FastAPI
- Streamlit
- ChromaDB
- OpenAI API
- pypdf
- python-pptx
- python-dotenv
- requests
- uvicorn

---

## 📁 Project Structure

```text
RAG_project/
│
├── app/
│   ├── main.py                         # FastAPI application entry point
│   ├── api/
│   │   └── routes.py                   # API endpoints
│   ├── core/
│   │   └── config.py                   # Project configuration and environment variables
│   ├── models/
│   │   └── schemas.py                  # Pydantic request schemas
│   └── services/
│       ├── rag_service.py              # RAG pipeline logic
│       ├── openai_service.py           # OpenAI embeddings and answer generation
│       └── vector_store_service.py     # ChromaDB vector store logic
│
├── ingest.py                           # Document ingestion and vector database creation
├── frontend.py                         # Streamlit user interface
├── requirements.txt                    # Python dependencies
├── README.md
│
├── data/                               # Local notes grouped by subject
│   ├── math/
│   ├── physics/
│   └── ...
│
└── chroma_db/                          # Local ChromaDB vector database
```

> `data/`, `chroma_db/`, `.env`, and `venv/` are local-only files and should not be committed to GitHub.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Tyshchenko-Oleksandra/RAG_project.git
cd RAG_project
```

### 2. Create and activate a virtual environment

For macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project root:

```bash
touch .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 📚 Add Study Materials

Create a `data` folder and organize notes by subject:

```text
data/
├── math/
│   └── lecture_1.pdf
├── physics/
│   └── lecture_1.pdf
└── chemistry/
    └── lecture_1.pdf
```

The folder name becomes the subject name used by the app.

Example:

```text
data/math/
```

will appear in the app as:

```text
math
```

---

## 🧠 Ingest Documents

Run:

```bash
python3 ingest.py
```

This will:

1. Read PDF/PPTX files from `data/`
2. Extract text from documents
3. Split documents into chunks
4. Create embeddings using the OpenAI API
5. Store chunks, embeddings, and metadata in ChromaDB

After successful ingestion, a local `chroma_db/` folder will be created.

---

## 🚀 Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🌐 Run the Frontend

Open a second terminal and activate the virtual environment again:

```bash
source venv/bin/activate
```

Then run:

```bash
streamlit run frontend.py
```

The app will open at:

```text
http://localhost:8501
```

---

## 🔌 API Endpoints

### `GET /`

Health check endpoint.

Example response:

```json
{
  "message": "University RAG API is running"
}
```

---

### `GET /subjects`

Returns available subjects from the vector database.

Example response:

```json
{
  "subjects": ["discrete", "math", "physics"]
}
```

---

### `POST /ask`

Answers a question based on the selected subject notes.

Example request:

```json
{
  "subject": "math",
  "question": "What does the lecture say about numerical series?"
}
```

Example response:

```json
{
  "answer": "The answer generated from the retrieved lecture context.",
  "sources": [
    {
      "source": "lecture_1.pdf",
      "subject": "math",
      "content_type": "pdf",
      "chunk_index": 0,
      "page": 3,
      "label": "lecture_1.pdf, сторінка 3"
    }
  ]
}
```

---

## 🧩 How It Works

The application follows a Retrieval-Augmented Generation pipeline:

```text
User question
↓
Create embedding for the question
↓
Search similar chunks in ChromaDB
↓
Retrieve relevant lecture fragments
↓
Send retrieved context to the language model
↓
Generate an answer
↓
Return answer with sources
```

The model does not answer only from its general knowledge.  
It receives relevant fragments from the uploaded lecture notes and generates an answer based on that context.

---

## 🧪 Example Questions

- What does the lecture say about numerical series?
- Explain the main definitions from this topic.
- Summarize this lecture.
- What formulas are mentioned in the notes?
- Which page explains this concept?
- Де використовуються множини?
- Що в конспекті сказано про числові ряди?
- Поясни основну ідею цієї теми простими словами.

---

## 🏗️ Backend Architecture

The backend is organized using a clean FastAPI structure.

### `app/main.py`

Creates the FastAPI application and connects API routes.

### `app/api/routes.py`

Contains API endpoints:

- `/`
- `/subjects`
- `/ask`

### `app/models/schemas.py`

Contains Pydantic schemas for request validation.

### `app/core/config.py`

Stores project configuration:

- OpenAI API key
- ChromaDB path
- collection name
- embedding model
- chat model

### `app/services/rag_service.py`

Contains the main RAG pipeline:

- search relevant notes
- build context
- generate final answer
- format sources

### `app/services/openai_service.py`

Handles OpenAI API calls:

- embedding creation
- answer generation

### `app/services/vector_store_service.py`

Handles ChromaDB connection and subject retrieval.

---

## ⚠️ Notes

This project is intended for educational use.

The assistant answers based on retrieved notes. If the necessary information is not found in the uploaded materials, the system should not invent an answer.

PDF files that are scanned images may require OCR support, which is not included in the current version.

The OpenAI API key should always be stored in `.env` and never committed to GitHub.

---

## 🗺️ Future Improvements

- File upload directly from the web interface
- OCR support for scanned PDFs
- Better chunking strategy
- Query rewriting for better retrieval
- Reranking retrieved chunks
- Local LLM support with Ollama
- Support for more document formats
- User authentication
- Deployed cloud version
- Docker support
- Improved frontend design
- Source preview with retrieved text snippets
- Evaluation system for RAG quality

---

## 👩‍💻 Author

Created by Oleksandra Tyshchenko.