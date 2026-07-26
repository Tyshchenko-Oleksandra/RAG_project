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

---

## 📁 Project Structure

```text
RAG_project/
│
├── app.py              # FastAPI backend
├── rag.py              # RAG logic: search + answer generation
├── ingest.py           # Document ingestion and vector database creation
├── frontend.py         # Streamlit user interface
├── requirements.txt    # Python dependencies
├── README.md
│
├── data/               # Local notes grouped by subject
│   ├── math/
│   ├── physics/
│   └── ...
│
└── chroma_db/          # Local ChromaDB vector database
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

will appear as:

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
2. Split documents into chunks
3. Create embeddings
4. Store them in ChromaDB

After successful ingestion, a local `chroma_db/` folder will be created.

---

## 🚀 Run the Backend

Start the FastAPI server:

```bash
uvicorn app:app --reload
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

### `GET /subjects`

Returns available subjects from the vector database.

Example response:

```json
{
  "subjects": ["math", "physics"]
}
```

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

## 🧪 Example Questions

- What does the lecture say about numerical series?
- Explain the main definitions from this topic.
- Summarize this lecture.
- What formulas are mentioned in the notes?
- Which page explains this concept?

---

## ⚠️ Notes

This project is intended for educational use.

The assistant answers based on retrieved notes. If the necessary information is not found in the uploaded materials, the system should not invent an answer.

PDF files that are scanned images may require OCR support, which is not included in the current version.

---

## 🗺️ Future Improvements

- File upload directly from the web interface
- OCR support for scanned PDFs
- Better chunking strategy
- Support for more document formats
- User authentication
- Deployed cloud version
- Improved frontend design
- Source preview with retrieved text snippets

---

## 👩‍💻 Author

Created by Oleksandra Tyshchenko.