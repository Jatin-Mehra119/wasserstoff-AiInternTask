# RAG Chat Application - Documentation

A sophisticated Retrieval-Augmented Generation (RAG) chat application that enables intelligent conversations with your documents.

## 🏗️ Architecture Overview

```mermaid
flowchart TD
  %% Client Layer
  subgraph "Client Layer"
    direction TB
    WebClient["Web Client (HTML/JS/CSS)"]:::ui
    StreamlitUI["MVP Streamlit UI"]:::ui
  end

  %% Backend Layer
  subgraph "Backend Layer"
    direction TB
    FastAPI["FastAPI Backend"]:::api
    subgraph routes["Routes"]
      direction TB
      MainRoutes["main_routes.py"]:::api
      UploadRoutes["upload_routes.py"]:::api
      ChatRoutes["chat_routes.py"]:::api
      StoreRoutes["store_routes.py"]:::api
    end
    Models["models.py"]:::api
    Utils["utils.py"]:::api
  end

  %% RAG Engine Layer
  subgraph "RAG Engine Layer"
    direction TB
    Config["config.py"]:::core
    CoreEngine["enhanced_vectordb.py"]:::core
  end

  %% Persistence Layer
  VectorStore[(Vector Store<br/>FAISS Index + Metadata)]:::store

  %% External Services
  subgraph "External Services"
    direction TB
    GROQ["GROQ Vision API"]:::external
    SentenceModel["SentenceTransformer Model"]:::external
  end

  %% Tests
  subgraph "Automated Tests"
    direction TB
    Tests1["test_api_endpoints.py"]:::tests
    Tests2["test_endpoints_pytest.py"]:::tests
  end

  %% Connections
  WebClient -->|"/api/*" fetch| FastAPI
  MainRoutes -->|serve static| WebClient
  StreamlitUI -->|in-process calls| CoreEngine
  FastAPI -->|calls RAG Engine| CoreEngine
  CoreEngine -->|read/write| VectorStore
  CoreEngine -->|OCR & LLM requests| GROQ
  CoreEngine -->|embedding requests| SentenceModel
  StoreRoutes -->|disk read/write| VectorStore

  %% Click Events
  click WebClient "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/frontend/index.html"
  click WebClient "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/frontend/script.js"
  click WebClient "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/frontend/style.css"
  click StreamlitUI "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/streamlit_rag_app.py"
  click FastAPI "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/main.py"
  click Models "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/models.py"
  click Utils "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/utils.py"
  click MainRoutes "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/routes/main_routes.py"
  click UploadRoutes "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/routes/upload_routes.py"
  click ChatRoutes "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/routes/chat_routes.py"
  click StoreRoutes "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/backend/routes/store_routes.py"
  click Config "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/rag_elements/config.py"
  click CoreEngine "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/rag_elements/enhanced_vectordb.py"
  click Tests1 "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/test/test_api_endpoints.py"
  click Tests2 "https://github.com/jatin-mehra119/wasserstoff-aiinterntask/blob/main/test/test_endpoints_pytest.py"

  %% Styles
  classDef ui fill:#E3F2FD,stroke:#1976D2,color:#0D47A1;
  classDef api fill:#E8F5E9,stroke:#388E3C,color:#1B5E20;
  classDef core fill:#FFF3E0,stroke:#FB8C00,color:#E65100;
  classDef store fill:#FFF9C4,stroke:#FBC02D,color:#F57F17;
  classDef external fill:#ECEFF1,stroke:#607D8B,color:#37474F;
  classDef tests fill:#F3E5F5,stroke:#8E24AA,color:#4A148C;
```

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- GROQ API key (for OCR and chat)

### Installation & Running
```bash
# Clone repository
git clone https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask.git
cd wasserstoff-AiInternTask

# Install dependencies
pip install -r requirements.txt

# Run FastAPI backend (Production)
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Open http://localhost:8000 in browser

# Alternative: Run Streamlit MVP
streamlit run streamlit_rag_app.py
```

## 🔧 Architecture Components

### Core RAG Engine (`rag_elements/`)
- **`enhanced_vectordb.py`** - Main RAG implementation with document processing, vector search, and AI integration
- **`config.py`** - Configuration management and settings

### FastAPI Backend (`backend/`)
- **`main.py`** - Application entry point and server configuration
- **`models.py`** - Pydantic data models and API schemas
- **`utils.py`** - Utilities, state management, and helpers
- **`routes/`** - Modular API endpoints:
  - `main_routes.py` - Frontend serving and health
  - `upload_routes.py` - Document upload and processing
  - `chat_routes.py` - Chat interface and AI responses
  - `store_routes.py` - Vector store persistence

### Frontend (`frontend/`)
- **`index.html`** - Main application UI
- **`style.css`** - Responsive design and styling
- **`script.js`** - Frontend logic and API integration

### Legacy MVP
- **`streamlit_rag_app.py`** - Original Streamlit implementation

## 📊 Data Flow

1. **Document Upload** → Text extraction → Chunking → Vector embeddings → FAISS index
2. **Chat Query** → Semantic search → Context retrieval → AI response generation → Citations
3. **Persistence** → Save/load vector stores with metadata

## 🔌 Key APIs

- `POST /upload-files` - Process documents
- `POST /chat` - Chat with documents
- `GET /stats` - Processing statistics
- `POST /save-vector-store` - Persist data
- `POST /load-vector-store` - Restore data

## 🧪 Testing

```bash
cd tests
bash run_tests.sh
```

## 📚 External Dependencies

- **FAISS** - Vector similarity search
- **GROQ** - Vision OCR and conversational AI
- **LangChain** - Document processing
- **FastAPI** - Web framework
- **Sentence Transformers** - Text embeddings

For detailed information, see the main [README.md](../README.md).
