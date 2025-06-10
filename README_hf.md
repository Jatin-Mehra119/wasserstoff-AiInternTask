---
title: Wasserstoff AiInternTask
emoji: 🏃
colorFrom: green
colorTo: indigo
sdk: docker
pinned: false
license: apache-2.0
---

# RAG CHAT APPLICATION

A comprehensive Retrieval-Augmented Generation (RAG) chat application with document processing capabilities. The core RAG implementation is built in `enhanced_vectordb.py`, with a FastAPI backend and a modern web frontend.

## 🚀 Features

- **Multi-format Document Processing**: Support for PDFs, text files, images (with OCR), and more
- **Advanced Vector Search**: FAISS-powered similarity search with citation tracking
- **Theme Analysis**: AI-powered analysis of common themes across search results
- **Interactive Chat Interface**: Real-time chat with document-based responses
- **Processing Statistics**: Detailed metrics and visualizations
- **Vector Store Management**: Save and load processed document collections
- **Dual Implementation**: Core RAG engine in `enhanced_vectordb.py` with FastAPI backend (Streamlit was MVP)

## 📋 Supported File Types

- **Documents**: PDF, TXT, MD, PY, JS, HTML, CSV, JSON
- **Images**: PNG, JPG, JPEG, BMP, TIFF, WEBP (with OCR)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- GROQ API key (for OCR and chat capabilities)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask.git
   cd wasserstoff-AiInternTask
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🖥️ Running the Application

### FastAPI + HTML/JS Frontend (Primary Implementation)

The main application uses a FastAPI backend with a modern web frontend developed with assistance from Claude AI.

#### Automatic Launch
- **Linux/macOS**: `./run.sh`
- **Windows**: `run.bat`

#### Manual Launch
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open http://localhost:8000 in your browser.

### Streamlit Frontend (MVP Version)

The original Streamlit implementation served as the MVP (Minimum Viable Product):

```bash
streamlit run streamlit_rag_app.py
```

## 🎯 Usage

### 1. Set API Key
- Enter your GROQ API key in the configuration section
- This enables OCR for images and AI-powered chat responses

### 2. Upload Documents
- **File Upload**: Select multiple files using the file picker
- **Directory Processing**: Enter a directory path to process all supported files
- Supported formats: PDF, text files, images, and more

### 3. Process Documents
- Click "Process Documents" to analyze uploaded files
- The system will:
  - Extract text from all documents
  - Perform OCR on images
  - Create document chunks for better search
  - Build a vector database for similarity search

### 4. Chat with Documents
- Ask questions about your uploaded documents
- Get AI-powered responses with:
  - Direct answers based on document content
  - Citations showing source information
  - Theme analysis across multiple documents

### 5. Manage Vector Store
- **Save**: Persist processed documents for future use
- **Load**: Restore previously processed document collections

## 📊 Features Breakdown

### Document Processing
- **Multi-format Support**: Handles text, PDFs, images, and code files seamlessly
- **OCR Capabilities**: Extracts text from images using GROQ Vision API
- **Intelligent Chunking**: Text splitting optimized for search and retrieval
- **Metadata Preservation**: Tracks source files, types, processing timestamps
- **Batch Processing**: Handles multiple files simultaneously with progress tracking
- **Directory Scanning**: Recursive processing of entire directory structures
- **File Type Detection**: Automatic identification and appropriate processing
- **Error Recovery**: Graceful handling of corrupted or unsupported files

### Search & Retrieval
- **Semantic Search**: Uses sentence transformers for meaning-based search
- **Citation Tracking**: Provides exact source references with file paths and types
- **Relevance Scoring**: Shows confidence scores for search results
- **Multi-document Analysis**: Finds connections across different sources
- **Top-K Results**: Returns top 5 most relevant document chunks per query
- **Enhanced Metadata**: Preserves source file information, document types, and processing timestamps

### AI-Powered Analysis
- **Theme Extraction**: Identifies common topics across search results using LLM
- **Response Generation**: Creates comprehensive markdown-formatted answers
- **Context Synthesis**: Combines information from multiple document sources
- **Intelligent Fallback**: Provides structured responses even without LLM access
- **Citation Integration**: Seamlessly weaves source references into responses
- **Markdown Formatting**: Rich text responses with proper formatting, lists, and emphasis

### User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live processing status and statistics display
- **Visual Analytics**: Charts showing file type distribution and processing metrics
- **Interactive Chat**: Smooth conversation experience with instant responses
- **Citation Display**: Click-through citations with source file information
- **History Management**: Complete chat history with timestamps and persistence
- **Error Handling**: User-friendly error messages and status indicators
- **Progress Tracking**: Visual feedback during file processing and uploads

## 🔧 Backend Architecture & Core Implementation

### Core RAG Engine: `enhanced_vectordb.py`

The heart of the application lies in `enhanced_vectordb.py`, which implements the complete RAG (Retrieval-Augmented Generation) pipeline:

#### Key Components:
- **Document Processing Pipeline**: Multi-format document ingestion and text extraction
- **Vector Database Management**: FAISS-powered vector store with metadata tracking
- **Embedding Generation**: Sentence transformer-based document embeddings
- **Semantic Search**: Similarity-based document retrieval with relevance scoring
- **AI Integration**: GROQ API integration for OCR and chat capabilities
- **Theme Analysis**: LLM-powered theme extraction across search results

#### Core Features:
```python
# Main functionality in enhanced_vectordb.py
class EnhancedDocumentProcessor:
    - process_documents()      # Multi-format document processing
    - create_vector_store()    # FAISS vector database creation
    - search_documents()       # Semantic similarity search
    - get_chat_response()      # AI-powered response generation
    - save_vector_store()      # Persistent storage
    - load_vector_store()      # State restoration
```

### FastAPI Backend Structure

The backend is organized into modular components:

#### Backend Structure:
```
backend/
├── main.py                 # FastAPI application entry point and configuration
├── models.py               # Pydantic data models and schemas
├── utils.py                # Utility functions and helpers
└── routes/                 # Modular route handlers
    ├── main_routes.py      # Frontend serving and health checks
    ├── upload_routes.py    # Document upload and processing endpoints
    ├── chat_routes.py      # Chat interface and AI response handling
    └── store_routes.py     # Vector store management endpoints
```

#### Core Dependencies Integration:
- **enhanced_vectordb.py**: Core RAG implementation
- **GROQ API**: Vision OCR and chat LLM capabilities
- **FAISS**: High-performance vector similarity search
- **LangChain**: Document processing and text splitting
- **Sentence Transformers**: Text embedding generation

### API Documentation

The FastAPI backend provides a comprehensive REST API. When running, visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Core Endpoints

#### Authentication & Configuration
- `POST /api/set-api-key`: Configure GROQ API key
  - **Body**: `{"api_key": "your_groq_api_key"}`
  - **Response**: Status confirmation

#### Document Processing
- `POST /api/upload-files`: Upload and process multiple files
  - **Input**: Multipart form data with file uploads
  - **Response**: Processing statistics and success status
  - **Features**: Handles multiple file formats, creates vector store, provides detailed statistics

- `POST /api/process-directory`: Process documents from a directory path
  - **Body**: Form data with `directory_path` field
  - **Response**: Processing statistics and success status
  - **Features**: Recursive directory processing, automatic file type detection

#### Chat & Interaction
- `POST /api/chat`: Send chat message and get AI-powered response
  - **Body**: `{"message": "your question"}`
  - **Response**: Comprehensive chat response with citations and theme analysis
  - **Features**: 
    - Semantic search across processed documents
    - AI-generated responses with markdown formatting
    - Source citations with relevance scores
    - Theme analysis across multiple documents
    - Automatic chat history tracking

#### Data Management
- `GET /api/stats`: Get current processing statistics
  - **Response**: File counts, document counts, chunk counts, file type distribution
  
- `GET /api/chat-history`: Retrieve complete chat conversation history
  - **Response**: Array of chat exchanges with timestamps

- `DELETE /api/clear-chat`: Clear chat history
  - **Response**: Confirmation of history deletion

#### Vector Store Management
- `POST /api/save-vector-store`: Persist current vector store to disk
  - **Response**: Success confirmation
  - **Storage**: Saves to `./vector_store/` directory with metadata

- `POST /api/load-vector-store`: Load previously saved vector store
  - **Response**: Success confirmation with restored statistics
  - **Features**: Automatically restores processing statistics and metadata

#### Frontend Serving
- `GET /`: Serve the main HTML application interface
  - **Response**: Complete web application frontend

### Data Models & Response Formats

#### Chat Response Format
```json
{
  "response": "AI-generated markdown response",
  "citations": [
    {
      "content": "relevant document excerpt",
      "citation": "source file path",
      "type": "file type",
      "score": "relevance score"
    }
  ],
  "themes": {
    "key_themes": ["theme1", "theme2"],
    "analysis": "theme analysis text"
  },
  "timestamp": "2025-06-07T10:30:00.123456"
}
```

#### Processing Statistics Format
```json
{
  "total_files": 10,
  "total_documents": 25,
  "total_chunks": 150,
  "file_types": ["pdf", "txt", "py", "md"],
  "type_counts": {"pdf": 5, "txt": 3, "py": 1, "md": 1},
  "processed_at": "2025-06-07 10:30:00"
}
```

#### Error Response Format
```json
{
  "detail": "Error description message"
}
```

## 📁 Project Architecture

```
wasserstoff-AiInternTask/
├── rag_elements/                # Core RAG implementation
│   ├── enhanced_vectordb.py    # CORE RAG ENGINE - Main implementation
│   └── config.py               # Configuration management
├── backend/                     # FastAPI backend server
│   ├── main.py                 # Application entry point
│   ├── models.py               # Pydantic data models and schemas
│   ├── utils.py                # Backend utilities and helpers
│   ├── routes/                 # Modular API route handlers
│   │   ├── __init__.py         # Routes package initialization
│   │   ├── main_routes.py      # Frontend serving and health checks
│   │   ├── upload_routes.py    # Document upload and processing
│   │   ├── chat_routes.py      # Chat interface and AI responses
│   │   └── store_routes.py     # Vector store management
│   └── vector_store/           # Runtime vector database storage
│       ├── index.faiss         # FAISS vector index file
│       ├── index.pkl           # Index metadata and mappings
│       └── enhanced_metadata.json # Processing stats and file info
├── frontend/                   # Web interface (built with Claude AI assistance)
│   ├── index.html             # Main application interface
│   ├── style.css              # Modern responsive styling
│   └── script.js              # Frontend logic and API integration
├── streamlit_rag_app.py       # MVP Streamlit implementation
├── requirements.txt           # Python dependencies
├── LICENSE                    # Apache 2.0 License
└── README.md                  # Project documentation
```

### Core Implementation Focus

#### 🎯 `enhanced_vectordb.py` - The RAG Engine
This is where the magic happens. The file contains the complete RAG implementation:
- **Document Ingestion**: Multi-format processing (PDF, images, text, code)
- **Text Processing**: Intelligent chunking and metadata extraction
- **Vector Operations**: FAISS indexing and similarity search
- **AI Integration**: GROQ API for OCR and chat capabilities
- **State Management**: Save/load functionality for vector stores

#### 🚀 FastAPI Backend
Production-ready API server with:
- Async/await patterns for performance
- Modular route organization
- Comprehensive error handling
- Automatic API documentation
- CORS support for frontend integration

#### 🎨 Frontend (Claude AI Assisted)
Modern web interface featuring:
- Responsive design for all devices
- Real-time chat interface
- File upload with drag-and-drop
- Processing statistics and visualizations
- Citation display with source tracking

### Runtime Generated Files
The application creates additional files during operation:
```
backend/vector_store/           # Generated when processing documents
├── index.faiss               # FAISS vector similarity index
├── index.pkl                 # Index metadata and document mappings  
└── enhanced_metadata.json    # Processing statistics and file information
```

## 🔬 Technical Details

### Dependencies
- **LangChain**: Document processing and LLM integration
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings (all-MiniLM-L6-v2)
- **GROQ**: Vision API for OCR and chat LLM capabilities
- **FastAPI**: Backend API framework with automatic documentation
- **Streamlit**: Alternative frontend framework
- **Uvicorn**: ASGI server for FastAPI
- **Aiofiles**: Async file operations
- **Python-dotenv**: Environment variable management

### Processing Pipeline (`enhanced_vectordb.py`)
1. **Document Ingestion**: Load files and extract text content
   - Multi-format support: PDF, TXT, MD, PY, JS, HTML, CSV, JSON
   - Image OCR: PNG, JPG, JPEG, BMP, TIFF, WEBP using GROQ Vision API
2. **Text Chunking**: Split documents into searchable segments (800 chars with 100 overlap)
3. **Embedding Generation**: Create vector representations using sentence transformers
4. **Vector Store Creation**: Build FAISS index for fast similarity search
5. **Query Processing**: Find relevant chunks using semantic search (top-k=5)
6. **Theme Analysis**: AI-powered analysis of common themes across results using GROQ LLM
7. **Response Generation**: Synthesize markdown-formatted answers with citations

### Performance Considerations
- **Chunk Size**: Optimized at 800 characters with 100-character overlap
- **Embedding Model**: Uses efficient all-MiniLM-L6-v2 model (For accuracy use BAAI/bge-large-en-v1.5)
- **Vector Search**: FAISS provides fast similarity search with relevance scoring
- **Caching**: Vector stores can be saved/loaded with complete metadata preservation
- **Async Operations**: File uploads and processing use async/await patterns
- **Memory Management**: Automatic cleanup of temporary files and directories
- **Error Handling**: Comprehensive exception handling with detailed error messages

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.