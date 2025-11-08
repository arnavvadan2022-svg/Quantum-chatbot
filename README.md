# 🤖 Quantum RAG Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot that combines document retrieval with AI-powered responses to provide intelligent, context-aware answers based on your knowledge base.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Document Ingestion**: Upload and process various document formats (PDF, TXT, DOCX, etc.)
- **Vector Storage**: Efficient document embedding and storage using vector databases
- **Semantic Search**: Find relevant information using semantic similarity
- **Context-Aware Responses**: Generate accurate answers based on retrieved context
- **Conversational Interface**: Natural language interaction with chat history
- **REST API**: Easy integration with web and mobile applications
- **Scalable Architecture**: Built to handle large document collections

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Web Interface  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│   Flask API Server  │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Vector │ │ LLM Provider │
│  DB    │ │ (OpenAI/etc) │
└────────┘ └──────────────┘
```

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- API keys for LLM provider (OpenAI, Anthropic, etc.)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/arnavvadan2022-svg/Quantum-chatbot.git
cd Quantum-chatbot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
VECTOR_DB_PATH=./data/vectordb
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216
```

### 5. Initialize the Database

```bash
python init_db.py
```

## 💻 Usage

### Running the Application

```bash
# Start the Flask server
python app.py

# The server will start on http://localhost:5000
```

### Using the Chatbot

1. **Upload Documents**:
   ```bash
   curl -X POST -F "file=@document.pdf" http://localhost:5000/upload
   ```

2. **Ask Questions**:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"question": "What is quantum computing?"}' \
        http://localhost:5000/chat
   ```

3. **Web Interface**:
   - Open your browser and navigate to `http://localhost:5000`
   - Upload documents using the web interface
   - Start chatting with your documents

## 📁 Project Structure

```
Quantum-chatbot/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
│
├── models/                 # ML models and embeddings
│   ├── embeddings.py      # Document embedding logic
│   └── llm.py             # LLM integration
│
├── data/                   # Data storage
│   ├── vectordb/          # Vector database storage
│   └── documents/         # Processed documents
│
├── uploads/               # Temporary upload directory
│
├── utils/                 # Utility functions
│   ├── document_processor.py  # Document parsing
│   ├── vector_store.py        # Vector DB operations
│   └── helpers.py             # Helper functions
│
├── static/                # Static files (CSS, JS)
│   ├── css/
│   └── js/
│
├── templates/             # HTML templates
│   └── index.html
│
└── tests/                 # Unit tests
    ├── test_embeddings.py
    └── test_api.py
```

## ⚙️ Configuration

### requirements.txt

```txt
flask==3.0.0
langchain==0.1.0
langchain-community==0.0.10
openai==1.6.1
anthropic==0.8.1
chromadb==0.4.22
sentence-transformers==2.2.2
PyPDF2==3.0.1
python-docx==1.1.0
python-dotenv==1.0.0
tiktoken==0.5.2
faiss-cpu==1.7.4
numpy==1.24.3
pandas==2.0.3
```

### Supported Document Formats

- PDF (`.pdf`)
- Text files (`.txt`)
- Word documents (`.docx`)
- Markdown (`.md`)
- CSV (`.csv`)

## 🔍 How It Works

### 1. Document Ingestion
```python
# Documents are uploaded and processed
document → text extraction → chunking → embedding
```

### 2. Vector Storage
```python
# Embeddings are stored in vector database
text_chunks → embeddings → vector_db
```

### 3. Question Answering
```python
# User question is processed
question → embedding → similarity_search → context_retrieval → LLM → answer
```

### 4. RAG Pipeline
1. **Retrieve**: Find relevant document chunks using semantic search
2. **Augment**: Add retrieved context to the user's question
3. **Generate**: Use LLM to generate a contextual answer

## 🔌 API Endpoints

### POST /upload
Upload a document to the knowledge base.

**Request**:
```bash
curl -X POST -F "file=@document.pdf" http://localhost:5000/upload
```

**Response**:
```json
{
  "status": "success",
  "message": "Document uploaded and processed",
  "document_id": "abc123"
}
```

### POST /chat
Ask a question to the chatbot.

**Request**:
```json
{
  "question": "What is quantum computing?",
  "conversation_id": "optional-conv-id"
}
```

**Response**:
```json
{
  "answer": "Quantum computing is...",
  "sources": ["doc1.pdf", "doc2.pdf"],
  "conversation_id": "conv-123"
}
```

### GET /documents
List all uploaded documents.

**Response**:
```json
{
  "documents": [
    {
      "id": "doc1",
      "filename": "quantum.pdf",
      "uploaded_at": "2025-11-08T15:21:12Z"
    }
  ]
}
```

### DELETE /documents/:id
Delete a document from the knowledge base.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangChain for the RAG framework
- OpenAI for language models
- ChromaDB for vector storage
- Flask for the web framework

## 📧 Contact

**Arnav Vadan** - [@arnavvadan2022-svg](https://github.com/arnavvadan2022-svg)

Project Link: [https://github.com/arnavvadan2022-svg/Quantum-chatbot](https://github.com/arnavvadan2022-svg/Quantum-chatbot)

---

Made with ❤️ by Arnav Vadan
```
