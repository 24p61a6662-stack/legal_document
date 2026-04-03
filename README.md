# ⚖️ Legal Document Assistant

An AI-powered legal assistant that enables users to **upload, analyze, and query legal documents** using a Retrieval-Augmented Generation (RAG) pipeline powered by a local LLM (Mistral via Ollama). The system supports intelligent clause extraction, risk analysis, compliance checking, and natural language Q&A — all restricted strictly to the legal domain.

---

## 🌟 Features

- 📄 **Document Upload & Parsing** — Supports PDF, DOCX, and image files (OCR via Tesseract)
- 🔍 **RAG-Powered Q&A** — Ask questions about uploaded legal documents using semantic search + LLM generation
- ⚠️ **Risk Analysis** — Identifies potential legal risks within contracts and agreements
- ✅ **Compliance Checking** — Flags compliance concerns against regulatory standards
- 📑 **Contract Comparison** — Compare terms across multiple legal documents
- 🔐 **Domain Restriction** — System enforces strictly legal queries; non-legal questions are gracefully declined
- 🧩 **Modular Service Architecture** — Clean separation of concerns across chunking, embedding, retrieval, and generation layers

---

## 🏗️ Project Structure

```
legal_document/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point — chat & upload endpoints
│   │   ├── config.py            # Application configuration
│   │   ├── auth.py              # Authentication utilities
│   │   ├── api/
│   │   │   └── routes.py        # Additional API routes
│   │   ├── rag/
│   │   │   ├── ingest.py        # Document ingestion pipeline
│   │   │   └── rag_pipeline.py  # Core RAG logic (retrieval + generation)
│   │   ├── services/
│   │   │   ├── document_loader.py       # File loading and parsing
│   │   │   ├── chunker.py               # Text chunking strategy
│   │   │   ├── embedder_service.py      # Embedding generation
│   │   │   ├── vector_store.py          # ChromaDB vector store integration
│   │   │   ├── retriever.py             # Semantic document retrieval
│   │   │   ├── llm_service.py           # Ollama LLM integration
│   │   │   ├── risk_analyzer.py         # Legal risk identification
│   │   │   ├── compliance_checker.py    # Regulatory compliance analysis
│   │   │   └── contract_comparator.py  # Cross-document comparison
│   │   └── models/                      # Data models
│   ├── data/                            # Local document storage / vector data
│   ├── dataset.py                       # Dataset ingestion utilities (e.g., CUAD)
│   └── requirements.txt                 # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js               # Root React component
│   │   ├── api/                 # Axios API client
│   │   ├── auth/                # Authentication components
│   │   ├── components/          # Reusable UI components
│   │   └── pages/               # Page-level components
│   ├── public/
│   └── package.json             # Node.js dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Frontend    | React 18, Axios                      |
| Backend     | FastAPI, Uvicorn                     |
| AI / LLM    | Ollama (Mistral), LangChain          |
| Embeddings  | Sentence Transformers                |
| Vector DB   | ChromaDB                             |
| OCR         | Tesseract (via `pytesseract`)        |
| Auth        | Python-JOSE, Passlib (bcrypt)        |
| File Types  | PDF (`pypdf`), DOCX (`python-docx`), Images (Pillow) |

---

## ⚙️ Prerequisites

Before running the application, ensure the following are installed:

- **Python** 3.10+
- **Node.js** 18+ and npm
- **Ollama** — [Download here](https://ollama.com/download)
- **Tesseract OCR** — [Installation guide](https://github.com/tesseract-ocr/tesseract#installation)

Pull the required LLM model via Ollama:

```bash
ollama pull mistral
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd legal_document
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: `http://localhost:8000`

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will be available at: `http://localhost:3000`

### 5. Ensure Ollama is Running

In a separate terminal:

```bash
ollama serve
```

---

## 📡 API Endpoints

| Method | Endpoint  | Description                                  |
|--------|-----------|----------------------------------------------|
| POST   | `/chat`   | Submit a legal question for RAG-based Q&A    |
| POST   | `/upload` | Upload a PDF, DOCX, or image for AI analysis |

### Example — Chat Request

```json
POST /chat
{
  "question": "What are the termination clauses in this contract?"
}
```

### Example — File Upload

```
POST /upload
Content-Type: multipart/form-data

file: <your-legal-document.pdf>
```

---

## 🔒 Domain Enforcement

This assistant is **strictly limited to legal topics**. Queries that do not contain legally relevant keywords (e.g., contract, liability, compliance, jurisdiction, etc.) will receive a professional out-of-scope response. This ensures the system remains accurate and purpose-built.

---

## 📦 Dependencies

### Backend (`requirements.txt`)

```
fastapi
uvicorn
langchain
langchain-community
sentence-transformers
chromadb
pydantic
python-multipart
pypdf
python-docx
ollama
python-jose
passlib[bcrypt]
```

### Frontend (`package.json`)

```
react: ^18.2.0
react-dom: ^18.2.0
axios: ^1.6.0
react-scripts: 5.0.1
```

---

## 🧪 Document Analysis Output Format

When a document is uploaded, the AI returns a structured legal analysis:

1. **Document Summary** — High-level overview of the document
2. **Key Legal Clauses Identified** — Extracted clauses with context
3. **Potential Legal Risks** — Risks and red flags found in the document
4. **Important Observations** — Notable findings and recommendations

---

## 📄 License

This project is intended for educational and research purposes. Always consult a qualified legal professional for actual legal advice.

---

## 🤝 Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

---

*Built with ❤️ using FastAPI, React, LangChain, and Ollama.*
