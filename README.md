# 🤖 Quantum RAG Chatbot + TwinFlash AI

A powerful Retrieval-Augmented Generation (RAG) chatbot that combines document retrieval with AI-powered responses, now featuring **TwinFlash AI** - an advanced Digital Twin architecture for intelligent SSD management using Reinforcement Learning.

## 📋 Table of Contents

- [Features](#features)
- [TwinFlash AI Architecture](#twinflash-ai-architecture)
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

### RAG Chatbot Features
- **Document Ingestion**: Upload and process various document formats (PDF, TXT, DOCX, etc.)
- **Vector Storage**: Efficient document embedding and storage using vector databases
- **Semantic Search**: Find relevant information using semantic similarity
- **Context-Aware Responses**: Generate accurate answers based on retrieved context
- **Conversational Interface**: Natural language interaction with chat history
- **REST API**: Easy integration with web and mobile applications
- **Scalable Architecture**: Built to handle large document collections

### TwinFlash AI Features
- **Digital Twin SSD Simulation**: Virtual mirror of physical storage devices
- **Counterfactual RL Engine**: Simulates multiple future scenarios for optimal decision-making
- **Predictive Models**: Wear, latency, and error prediction models
- **Safety Mechanisms**: Confidence thresholds and fallback rules prevent risky actions
- **Continuous Learning**: Self-improving system that learns from outcomes
- **Real-time Telemetry**: Live monitoring of SSD health and performance

## 🏗️ TwinFlash AI Architecture

TwinFlash AI implements a sophisticated 6-layer architecture for intelligent SSD management:

```
Input → Twin → Simulation → Intelligence → Execution → Feedback

┌─────────────────────────────────────────────────────────────┐
│                    TWINFLASH AI SYSTEM                      │
└─────────────────────────────────────────────────────────────┘

Layer 1: Real SSD Layer (Physical Layer)
├── Role: Interface with actual storage device
├── Provides: Live Storage Telemetry
└── Components: Read/Write Ops, Block Status, Wear Counters, 
    Error Logs, Temperature, I/O Workload

Layer 2: State Synchronization Layer
├── Role: Keep Digital Twin updated with real SSD
├── Provides: S(t) = Current SSD State
└── Techniques: Log Mirroring, Event Streaming, Periodic Snapshots

Layer 3: Digital Twin Layer (Simulation Engine)
├── Role: Virtual SSD in software
├── Provides: S(t+1) = Predicted State
└── Models:
    ├── Wear Model: Predicts erase cycle impact & block degradation
    ├── Latency Model: Predicts read/write delay & queue congestion
    └── Error Model: Predicts bit error rate, retention loss, ECC failures

Layer 4: Counterfactual RL Layer (Decision Engine) [BRAIN]
├── Role: Runs multiple "parallel futures"
├── Provides: A* = Optimal Action
└── Components:
    ├── Action Generator: Generates possible actions
    ├── Parallel Simulator: Creates Future_i = Twin(S(t), A_i)
    ├── Evaluation Engine: Measures wear, latency, error, lifetime, energy
    └── RL Policy Network: Learns π(S) → A* using DQN/PPO

Layer 5: Decision & Execution Layer
├── Role: Applies AI decision to real SSD
├── Provides: Action Execution
├── Actions: Firmware commands, compression, GC, mapping updates
└── Safety: If confidence < threshold → fallback rules

Layer 6: Feedback & Learning Layer (Self-Improvement)
├── Role: Makes system smarter over time
├── Provides: Model Updates
└── Loop: Prediction → Reality → Error → Learning (continuous)
```

### Data Flow Pipeline

```
Real SSD
   ↓ [Telemetry]
State Sync
   ↓ [S(t)]
Digital Twin
   ↓ [Parallel Simulations]
RL Simulator
   ↓ [Evaluated Futures]
Evaluation Engine
   ↓ [Scores]
Decision Unit
   ↓ [Optimal Action A*]
Firmware Executor
   ↓ [Execution Result]
Feedback Logger
   ↺ [Learning Loop back to Twin]
```

### Why This Architecture Is Powerful

| Feature        | Traditional SSD | TwinFlash AI |
|----------------|-----------------|--------------|
| Decision Making| Static          | Adaptive     |
| Learning       | No              | Yes          |
| Simulation     | No              | Yes          |
| Prediction     | No              | Yes          |
| Safety         | Limited         | High         |

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

### Using TwinFlash AI

1. **Demo TwinFlash**:
   ```bash
   python test_twinflash.py
   ```
   
   This will run a comprehensive demo showing:
   - Architecture overview
   - Single lifecycle execution
   - Continuous operation (5 cycles)
   - System status and statistics

2. **API Usage**:

   **Get TwinFlash Status**:
   ```bash
   curl http://localhost:5000/api/twinflash/status
   ```

   **Get Architecture Info**:
   ```bash
   curl http://localhost:5000/api/twinflash/architecture
   ```

   **Run Single Lifecycle**:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"simulate_workload": true}' \
        http://localhost:5000/api/twinflash/run-lifecycle
   ```

   **Run Continuous Cycles**:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"num_cycles": 5}' \
        http://localhost:5000/api/twinflash/run-continuous
   ```

   **Get SSD Statistics**:
   ```bash
   curl http://localhost:5000/api/twinflash/ssd-stats
   ```

## 📁 Project Structure

```
Quantum-chatbot/
│
├── app.py                  # Main Flask application
├── test_twinflash.py      # TwinFlash demo script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
│
├── src/                    # Source code
│   ├── arxiv_search.py    # arXiv paper search
│   ├── google_search.py   # Google search integration
│   ├── serpapi_search.py  # SerpAPI integration
│   ├── web_scraper.py     # Web scraping
│   ├── query_processor.py # Query processing
│   ├── rag_engine.py      # RAG engine
│   │
│   └── twinflash/         # TwinFlash AI modules
│       ├── __init__.py
│       ├── ssd_layer.py           # Real SSD Layer (Physical)
│       ├── state_sync.py          # State Synchronization
│       ├── digital_twin.py        # Digital Twin (Simulation)
│       ├── rl_engine.py           # Counterfactual RL Engine
│       ├── decision_executor.py   # Decision & Execution
│       ├── feedback_logger.py     # Feedback & Learning
│       └── twinflash_core.py      # Core System Orchestration
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
