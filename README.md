# 🤖 RAG CHAT APPLICATION

A sophisticated Retrieval-Augmented Generation (RAG) chat application that enables intelligent conversations with your documents. Built with a modular architecture featuring a FastAPI backend, modern web frontend, and powerful document processing capabilities.

## ✨ Key Highlights

- 🚀 **Production-Ready FastAPI Backend** with comprehensive REST API
- 🎨 **Modern Web Frontend** with responsive design and real-time chat
- 📚 **Core RAG Engine** in `enhanced_vectordb.py` - the heart of the application
- 🔍 **Advanced Document Processing** with OCR, semantic search, and AI analysis
- ⚡ **High Performance** with FAISS vector search and async operations
- 💾 **Persistent Storage** for vector stores and chat history
- 📊 **Comprehensive Analytics** with processing statistics and visualizations

## 🚀 Features

- **Multi-format Document Processing**: PDFs, text files, images (OCR), code files, and more
- **Advanced Vector Search**: FAISS-powered semantic similarity search with citation tracking
- **AI-Powered Analysis**: Theme extraction and intelligent response generation using GROQ API
- **Interactive Chat Interface**: Real-time conversations with document-based context
- **Processing Statistics**: Detailed metrics, file type analysis, and performance visualizations
- **Vector Store Management**: Save and load processed document collections with metadata
- **Dual Implementation**: Production FastAPI backend + legacy Streamlit MVP for comparison

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

### 🎯 FastAPI + Web Frontend (Production)

The main application uses a modern FastAPI backend with an HTML/CSS/JavaScript frontend.

#### Quick Start
```bash
# Navigate to backend directory
cd backend

# Run the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open **http://localhost:8000** in your browser.

#### Alternative Launch Methods
- **Linux/macOS**: `./run.sh` (if available)
- **Windows**: `run.bat` (if available)
- **Docker**: `docker build -t rag-app . && docker run -p 8000:8000 rag-app` (if Dockerfile is configured)

### 📱 Streamlit MVP Version

The original Streamlit implementation (MVP - Minimum Viable Product):

```bash
streamlit run streamlit_rag_app.py
```

**Note**: The FastAPI version is the primary, production-ready implementation. The Streamlit version serves as a reference MVP.

## 🎯 Usage Guide

### 1. 🔑 Configure API Key
- Navigate to the configuration section in the web interface
- Enter your **GROQ API key** to enable:
  - OCR processing for image documents
  - AI-powered chat responses and theme analysis
  - Advanced document understanding capabilities

### 2. 📤 Upload Documents
Choose from two upload methods:

#### File Upload
- Click "Choose Files" or drag-and-drop files into the upload area
- Select multiple files simultaneously for batch processing
- Supported formats: PDF, TXT, MD, PY, JS, HTML, CSV, JSON, PNG, JPG, etc.

#### Directory Processing
- Enter an absolute directory path (e.g., `/path/to/documents/`)
- Enable recursive processing to include subdirectories
- All supported files will be automatically detected and processed

### 3. ⚙️ Process Documents
Click "Process Documents" to initiate the RAG pipeline:
- **Text Extraction**: Extract content from all document types
- **OCR Processing**: Convert images to searchable text using GROQ Vision API
- **Document Chunking**: Split content into optimal segments for search
- **Vector Generation**: Create semantic embeddings using sentence transformers
- **Index Building**: Construct FAISS vector database for fast similarity search
- **Metadata Tracking**: Preserve source information, file types, and processing statistics

### 4. 💬 Chat with Your Documents
Start asking questions about your uploaded content:
- **Natural Language Queries**: Ask questions in plain English
- **Contextual Responses**: Get AI-generated answers based on document content
- **Source Citations**: View exact references with file paths and relevance scores
- **Theme Analysis**: Discover common topics across multiple documents
- **Chat History**: Access complete conversation history with timestamps

### 5. 💾 Manage Vector Store
Persist your processed documents:
- **Save**: Store the current vector database to disk for future sessions
- **Load**: Restore previously processed document collections instantly
- **Statistics**: View detailed processing metrics and file type distributions

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

### 🔧 Backend Architecture & Core Implementation

The application follows a modular, production-ready architecture with clear separation of concerns:

### 🎯 Core RAG Engine: `enhanced_vectordb.py`

The heart of the application - a comprehensive RAG implementation that handles the entire document-to-chat pipeline:

#### Key Components:
- **📄 Document Processing Pipeline**: Multi-format document ingestion and intelligent text extraction
- **🔢 Vector Database Management**: FAISS-powered vector store with comprehensive metadata tracking
- **🧠 Embedding Generation**: Advanced sentence transformer-based document embeddings
- **🔍 Semantic Search**: Intelligent similarity-based document retrieval with confidence scoring
- **🤖 AI Integration**: Seamless GROQ API integration for OCR and conversational AI
- **📊 Theme Analysis**: LLM-powered pattern recognition and theme extraction across documents

#### Core Class Structure:
```python
class EnhancedDocumentProcessor:
    # Document Processing
    def process_files(self, file_paths)              # Multi-format file processing
    def process_directory(self, directory_path)      # Recursive directory processing
    
    # Vector Operations
    def create_enhanced_vector_store(self, documents) # FAISS index creation with metadata
    def search_with_citations(self, query, k=5)      # Semantic search with source tracking
    
    # AI-Powered Features
    def analyze_themes(self, query, search_results)   # Theme extraction using LLM
    def get_chat_response(self, query)                # End-to-end chat response generation
    
    # Persistence
    def save_vector_store(self, path)                 # Save vector store with metadata
    def load_vector_store(self, path)                 # Load saved vector store
```

### 🌐 FastAPI Backend Structure

Modern, scalable backend architecture with clean separation of concerns:

#### Backend Organization:
```
backend/
├── main.py                 # 🚀 FastAPI app initialization, CORS, and server config
├── models.py               # 📋 Pydantic data models and API schemas
├── utils.py                # 🛠️ Core utilities, state management, and helpers
└── routes/                 # 📍 Modular API endpoint handlers
    ├── __init__.py         # Package initialization and router exports
    ├── main_routes.py      # 🏠 Frontend serving and application health
    ├── upload_routes.py    # 📤 Document upload and processing logic
    ├── chat_routes.py      # 💬 Chat interface and AI response handling
    └── store_routes.py     # 💾 Vector store persistence and management
```

#### Key Integration Points:
- **🔌 enhanced_vectordb.py**: Core RAG engine integration
- **🤖 GROQ API**: Vision OCR and conversational AI capabilities
- **⚡ FAISS**: High-performance vector similarity search
- **🔗 LangChain**: Advanced document processing and text manipulation
- **🧠 Sentence Transformers**: State-of-the-art text embedding generation
- **🌍 FastAPI**: Async/await patterns with automatic OpenAPI documentation

### 📖 API Documentation

The FastAPI backend provides comprehensive, interactive API documentation:
- **📚 Swagger UI**: http://localhost:8000/docs
- **📄 ReDoc**: http://localhost:8000/redoc
- **🔧 OpenAPI Schema**: Auto-generated from code with full type hints

### Core Endpoints

#### Authentication & Configuration
- `POST /set-api-key`: Configure GROQ API key
  - **Body**: `{"api_key": "your_groq_api_key"}`
  - **Response**: Status confirmation

#### Document Processing
- `POST /upload-files`: Upload and process multiple files
  - **Input**: Multipart form data with file uploads
  - **Response**: Processing statistics and success status
  - **Features**: Handles multiple file formats, creates vector store, provides detailed statistics

- `POST /process-directory`: Process documents from a directory path
  - **Body**: Form data with `directory_path` field
  - **Response**: Processing statistics and success status
  - **Features**: Recursive directory processing, automatic file type detection

#### Chat & Interaction
- `POST /chat`: Send chat message and get AI-powered response
  - **Body**: `{"message": "your question"}`
  - **Response**: Comprehensive chat response with citations and theme analysis
  - **Features**: 
    - Semantic search across processed documents
    - AI-generated responses with markdown formatting
    - Source citations with relevance scores
    - Theme analysis across multiple documents
    - Automatic chat history tracking

#### Data Management & Analytics
- `GET /stats`: Get current processing statistics
  - **Response**: File counts, document counts, chunk counts, file type distribution
  
- `GET /chat-history`: Retrieve complete chat conversation history
  - **Response**: Array of chat exchanges with timestamps

- `DELETE /clear-chat`: Clear chat history and reset session
  - **Response**: Confirmation of history deletion

#### Vector Store Management
- `POST /save-vector-store`: Persist current vector store to disk
  - **Response**: Success confirmation
  - **Storage**: Saves to `./vector_store/` directory with enhanced metadata

- `POST /load-vector-store`: Load previously saved vector store
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
├── 🧠 rag_elements/                # Core RAG Implementation
│   ├── enhanced_vectordb.py       # ⭐ MAIN RAG ENGINE - Complete implementation
│   └── config.py                  # Configuration and settings management
│
├── 🚀 backend/                    # Production FastAPI Server
│   ├── main.py                    # Application entry point and server config
│   ├── models.py                  # Pydantic schemas and data models
│   ├── utils.py                   # Utilities, state management, and helpers
│   ├── routes/                    # Modular API endpoint handlers
│   │   ├── __init__.py            # Router exports and package init
│   │   ├── main_routes.py         # Frontend serving and health endpoints
│   │   ├── upload_routes.py       # Document upload and processing APIs
│   │   ├── chat_routes.py         # Chat interface and AI response APIs
│   │   └── store_routes.py        # Vector store management APIs
│   └── vector_store/              # 💾 Runtime vector database storage
│       ├── index.faiss            # FAISS vector similarity index
│       ├── index.pkl              # Index metadata and document mappings
│       └── enhanced_metadata.json # Processing stats and file information
│
├── 🎨 frontend/                   # Modern Web Interface
│   ├── index.html                 # Main application UI and layout
│   ├── style.css                  # Responsive design and modern styling
│   └── script.js                  # Frontend logic and API integration
│
├── 📱 streamlit_rag_app.py        # Legacy MVP Implementation (Streamlit)
├── 📋 requirements.txt            # Python dependencies and versions
├── 📄 LICENSE                     # Apache 2.0 License
├── 🐳 Dockerfile                  # Container deployment configuration
└── 📖 README.md                   # Comprehensive project documentation
```

### 🎯 Core Implementation Focus

#### ⭐ `enhanced_vectordb.py` - The RAG Engine
**This is where the magic happens.** The complete RAG implementation including:
- 📄 **Document Ingestion**: Multi-format processing (PDF, images, text, code)
- ✂️ **Text Processing**: Intelligent chunking and metadata extraction  
- 🔢 **Vector Operations**: FAISS indexing and semantic similarity search
- 🤖 **AI Integration**: GROQ API for OCR and conversational capabilities
- 💾 **State Management**: Save/load functionality for vector stores
- 📊 **Analytics**: Processing statistics and performance metrics

#### 🚀 FastAPI Backend (Production)
Enterprise-ready API server featuring:
- ⚡ **Async/Await Patterns**: High-performance async operations
- 📍 **Modular Architecture**: Clean separation of concerns with organized routes
- 🛡️ **Error Handling**: Comprehensive exception handling and logging
- 📚 **Auto Documentation**: Interactive OpenAPI/Swagger documentation
- 🌍 **CORS Support**: Cross-origin resource sharing for frontend integration
- 🔌 **Hot Reload**: Development server with automatic code reloading

#### 🎨 Frontend (Modern Web UI)
Professional web interface with:
- 📱 **Responsive Design**: Mobile-first approach for all device types
- 💬 **Real-time Chat**: WebSocket-like experience with instant responses
- 📤 **File Upload**: Drag-and-drop interface with progress indicators
- 📊 **Analytics Dashboard**: Processing statistics and data visualizations
- 🔗 **Citation System**: Interactive source references and document tracking
- 🎯 **UX/UI Excellence**: Modern design patterns and intuitive workflows

### 🎛️ Runtime Generated Files
The application creates additional files during operation:
```
backend/vector_store/              # 💾 Generated during document processing
├── index.faiss                  # FAISS vector similarity index (binary)
├── index.pkl                    # Index metadata and document mappings (pickle)  
└── enhanced_metadata.json       # Processing statistics and file information (JSON)
```

## 🔬 Technical Implementation Details

### 🧰 Core Dependencies & Technologies

#### 🤖 AI & Machine Learning
- **🔗 LangChain**: Advanced document processing and LLM integration framework
- **⚡ FAISS**: Facebook's high-performance vector similarity search library
- **🧠 Sentence Transformers**: State-of-the-art text embedding models (all-MiniLM-L6-v2)
- **🚀 GROQ**: Cutting-edge Vision API for OCR and conversational AI capabilities

#### 🌐 Backend & API
- **⚡ FastAPI**: Modern, fast async web framework with automatic OpenAPI documentation
- **🦄 Uvicorn**: Lightning-fast ASGI server for async Python applications
- **📁 Aiofiles**: Async file operations for improved I/O performance
- **🌍 Python-dotenv**: Environment variable management and configuration

#### 📊 Data Processing & Utilities  
- **🐼 Pandas**: Data manipulation and analysis (if CSV processing is needed)
- **🖼️ Pillow**: Image processing and manipulation library
- **📄 PyPDF2/pdfplumber**: PDF text extraction and processing
- **📋 Pydantic**: Data validation and settings management with type hints

### 🔄 Processing Pipeline Deep Dive (`enhanced_vectordb.py`)

#### 1. 📥 **Document Ingestion & Text Extraction**
   - **Multi-format Support**: PDF, TXT, MD, PY, JS, HTML, CSV, JSON
   - **Advanced OCR**: PNG, JPG, JPEG, BMP, TIFF, WEBP using GROQ Vision API
   - **Error Handling**: Graceful fallback for corrupted or unsupported files
   - **Metadata Tracking**: Source file paths, types, processing timestamps

#### 2. ✂️ **Intelligent Text Chunking**
   - **Optimal Chunk Size**: 800 characters with 100-character overlap for context preservation
   - **Smart Splitting**: Respects sentence boundaries and document structure
   - **Metadata Preservation**: Maintains source information throughout chunking process
   - **Memory Efficiency**: Streaming processing for large documents

#### 3. 🧠 **Embedding Generation & Vector Store Creation**
   - **Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings, good balance of speed/accuracy)
   - **Alternative**: `BAAI/bge-large-en-v1.5` (1024-dimensional, higher accuracy for production)
   - **FAISS Index**: Efficient L2 distance similarity search with IndexFlatL2
   - **Metadata Storage**: Parallel storage of document metadata for citation tracking

#### 4. 🔍 **Query Processing & Semantic Search**
   - **Top-K Retrieval**: Returns top 5 most relevant document chunks (configurable)
   - **Similarity Scoring**: L2 distance normalization for relevance ranking
   - **Citation Generation**: Automatic source attribution with file paths and confidence scores
   - **Result Filtering**: Duplicate removal and relevance threshold filtering

#### 5. 🎯 **AI-Powered Theme Analysis & Response Generation**
   - **Theme Extraction**: GROQ LLM analyzes common patterns across search results
   - **Context Synthesis**: Intelligent combination of multiple document sources
   - **Markdown Generation**: Rich text responses with proper formatting, lists, and emphasis
   - **Citation Integration**: Seamless source reference weaving within responses
   - **Fallback Handling**: Structured responses even without LLM access

### ⚡ Performance Optimizations & Considerations

#### 🚀 **Speed & Efficiency**
- **Chunk Size Optimization**: 800 characters balances context and search precision
- **Efficient Embedding Model**: all-MiniLM-L6-v2 provides fast inference with good quality
- **FAISS Performance**: In-memory vector search with sub-millisecond query times
- **Async Operations**: Non-blocking file uploads and processing using async/await patterns
- **Memory Management**: Automatic cleanup of temporary files and efficient garbage collection

#### 💾 **Storage & Caching**
- **Vector Store Persistence**: Complete save/load with metadata preservation
- **Metadata Compression**: JSON-based metadata storage with optional compression
- **Index Optimization**: FAISS index optimization for reduced memory footprint
- **Session Management**: Efficient state management across multiple user sessions

#### 🛡️ **Error Handling & Robustness**
- **Comprehensive Exception Handling**: Detailed error messages with context
- **File Type Validation**: Automatic file type detection and format verification
- **Resource Cleanup**: Automatic temporary file and directory cleanup
- **Graceful Degradation**: Fallback responses when AI services are unavailable
- **Input Sanitization**: Protection against malformed files and malicious inputs

#### 📊 **Monitoring & Analytics**
- **Processing Statistics**: Detailed metrics on file counts, chunk counts, and processing times
- **Performance Tracking**: Query response times and embedding generation speeds
- **Error Logging**: Comprehensive logging for debugging and monitoring
- **Usage Analytics**: Chat history tracking and user interaction patterns

## 🧪 Testing & Development

### 🔬 Running Tests
```bash
# Navigate to tests directory
cd tests

# Install test dependencies
pip install -r requirements-test.txt

# Run comprehensive test suite
bash run_tests.sh

# Or run individual test files
python -m pytest test_endpoints_pytest.py -v
python test_api_endpoints.py
```

### 🛠️ Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask.git
cd wasserstoff-AiInternTask

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env      # Create .env file
# Edit .env and add your GROQ_API_KEY

# Run in development mode
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🐳 Docker Deployment (if configured)
```bash
# Build the container
docker build -t rag-chat-app .

# Run the application
docker run -p 8000:8000 -e GROQ_API_KEY=your_key_here rag-chat-app

# Or use docker-compose (if docker-compose.yml exists)
docker-compose up -d
```

## 🤝 Contributing

### 🔧 Development Guidelines
1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Type Hints**: Use comprehensive type annotations
3. **Documentation**: Add docstrings for all functions and classes
4. **Testing**: Write tests for new features and bug fixes
5. **Error Handling**: Implement comprehensive exception handling

### 📝 Pull Request Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `bash tests/run_tests.sh`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request with a clear description

## 🎯 Future Enhancements

### 🚀 Planned Features
- **🔐 Authentication System**: User accounts and document access control
- **☁️ Cloud Storage Integration**: AWS S3, Google Drive, Dropbox support
- **📊 Advanced Analytics**: Usage metrics, query performance analytics
- **🌍 Multi-language Support**: International document processing
- **🔄 Real-time Collaboration**: Shared document spaces and collaborative chat
- **📱 Mobile App**: React Native or Flutter mobile application
- **🎨 Theming System**: Customizable UI themes and branding options

### 🔧 Technical Improvements
- **🗃️ Database Integration**: PostgreSQL/MongoDB for metadata storage
- **⚖️ Load Balancing**: Horizontal scaling for high-traffic deployment  
- **📈 Monitoring**: Comprehensive logging, metrics, and alerting
- **🔒 Security**: Enhanced security features, rate limiting, input validation
- **🌐 WebSocket Support**: Real-time chat updates and live document processing
- **🧠 Model Upgrades**: Integration with latest embedding and LLM models

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[📖 Documentation Index](docs/index.md)** - Complete documentation overview
- **[🏗️ Architecture & Quick Start](docs/README.md)** - Project architecture with mermaid diagram
- **[🔌 API Reference](docs/API.md)** - REST API endpoints and examples
- **[💻 Development Guide](docs/DEVELOPMENT.md)** - Contributing and development setup

### Interactive API Documentation
When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for complete details.

### 📋 License Summary
- ✅ **Commercial Use**: Free to use in commercial applications
- ✅ **Modification**: Modify and distribute modified versions
- ✅ **Distribution**: Distribute original or modified versions
- ✅ **Patent Grant**: Express patent grant from contributors
- ⚠️ **Attribution**: Must include original copyright and license notices
- ⚠️ **State Changes**: Document significant changes made to the code

---

## 🙏 Acknowledgments

- **🤖 GROQ**: For providing powerful Vision OCR and conversational AI APIs
- **⚡ FAISS**: Facebook AI Research for the exceptional vector similarity search library
- **🦄 FastAPI**: For the modern, fast, and developer-friendly web framework
- **🔗 LangChain**: For comprehensive document processing and LLM integration tools
- **🧠 Sentence Transformers**: For state-of-the-art text embedding models
- **🎨 Claude AI**: For assistance in developing the modern web frontend interface

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

**📧 Questions? Issues? Feel free to open an issue or reach out!**

**🚀 Happy RAG Chatting! 🚀**

</div>