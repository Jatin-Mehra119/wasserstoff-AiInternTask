# Agentic RAG Chat Application

A comprehensive Retrieval-Augmented Generation (RAG) chat application with document processing capabilities, featuring both Streamlit and FastAPI+HTML/JS implementations.

## 🚀 Features

- **Multi-format Document Processing**: Support for PDFs, text files, images (with OCR), and more
- **Advanced Vector Search**: FAISS-powered similarity search with citation tracking
- **Theme Analysis**: AI-powered analysis of common themes across search results
- **Interactive Chat Interface**: Real-time chat with document-based responses
- **Processing Statistics**: Detailed metrics and visualizations
- **Vector Store Management**: Save and load processed document collections
- **Dual Implementation**: Choose between Streamlit or FastAPI+HTML/JS frontend

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
   git clone <repository-url>
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

### Option 1: FastAPI + HTML/JS Frontend (Recommended)

#### Automatic Launch
- **Linux/macOS**: `./run.sh`
- **Windows**: `run.bat`

#### Manual Launch
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open http://localhost:8000 in your browser.

### Option 2: Streamlit Frontend

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

## 🔧 API Documentation

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

## 📁 Project Structure

```
wasserstoff-AiInternTask/
├── backend/
│   ├── main.py                 # FastAPI backend server with complete API
│   └── __pycache__/           # Python cache files
├── frontend/
│   ├── index.html             # Main HTML interface
│   ├── style.css              # Styling and responsive layout
│   └── script.js              # Frontend JavaScript logic and API integration
├── rag_elements/
│   ├── enhanced_vectordb.py   # Enhanced document processor with GROQ integration
│   ├── vectordb.py           # Basic document processor
│   └── __pycache__/          # Python cache files
├── streamlit_rag_app.py      # Alternative Streamlit implementation
├── requirements.txt          # Python dependencies
├── run.sh                   # Linux/macOS launcher script
├── run.bat                  # Windows launcher script
├── .env                     # Environment variables (create manually)
├── LICENSE                  # Apache 2.0 License
└── README.md               # This documentation file
```

### Generated Runtime Files
```
vector_store/                 # Created when saving vector stores
├── index.faiss             # FAISS vector index
├── index.pkl               # Index metadata
└── enhanced_metadata.json  # Processing statistics and file information
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

### Processing Pipeline
1. **Document Ingestion**: Load files and extract text content
   - Multi-format support: PDF, TXT, MD, PY, JS, HTML, CSV, JSON
   - Image OCR: PNG, JPG, JPEG, BMP, TIFF, WEBP
2. **Text Chunking**: Split documents into searchable segments (800 chars with 100 overlap)
3. **Embedding Generation**: Create vector representations using sentence transformers
4. **Vector Store Creation**: Build FAISS index for fast similarity search
5. **Query Processing**: Find relevant chunks using semantic search (top-k=5)
6. **Theme Analysis**: AI-powered analysis of common themes across results
7. **Response Generation**: Synthesize markdown-formatted answers using LLM

### Performance Considerations
- **Chunk Size**: Optimized at 800 characters with 100-character overlap
- **Embedding Model**: Uses efficient all-MiniLM-L6-v2 model
- **Vector Search**: FAISS provides fast similarity search with relevance scoring
- **Caching**: Vector stores can be saved/loaded with complete metadata preservation
- **Async Operations**: File uploads and processing use async/await patterns
- **Memory Management**: Automatic cleanup of temporary files and directories
- **Error Handling**: Comprehensive exception handling with detailed error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**:
   - Ensure GROQ API key is valid and has sufficient credits
   - Check internet connection for API requests
   - Verify API key permissions for vision and chat models
   - Use the `/api/set-api-key` endpoint or set `GROQ_API_KEY` environment variable

2. **File Processing Fails**:
   - Check file format compatibility (see supported formats above)
   - Ensure files aren't corrupted or password-protected
   - Verify sufficient disk space for temporary file processing
   - Check file permissions for read access

3. **Vector Store Loading Issues**:
   - Ensure `vector_store/` directory exists in the project root
   - Check file permissions for the vector store directory
   - Verify vector store was saved properly with metadata
   - Look for `enhanced_metadata.json` file in the vector store directory

4. **Chat Not Working**:
   - Confirm documents are processed first (check `/api/stats` endpoint)
   - Verify API key is set and valid
   - Ensure backend server is running on port 8000
   - Check browser console for JavaScript errors

5. **Upload Failures**:
   - Check file size limits (default FastAPI limits apply)
   - Ensure proper file extensions
   - Verify CORS settings for cross-origin requests
   - Monitor server logs for detailed error messages

6. **Memory Issues**:
   - Large documents may require more RAM
   - Process files in smaller batches
   - Monitor system memory usage during processing
   - Consider restarting the application for memory cleanup

### Performance Tips

- **Large Documents**: Process in smaller batches for better performance and memory management
- **Memory Usage**: Monitor RAM usage with large document collections (each chunk requires embedding storage)
- **Storage**: Vector stores can be large - ensure sufficient disk space (typically 100-500MB per 1000 documents)
- **Network**: Stable internet connection required for GROQ API calls during OCR and chat
- **Concurrent Processing**: The system handles multiple file uploads efficiently but processes them sequentially
- **Cache Management**: Vector stores persist between sessions - use save/load functionality for large collections

## 🚀 Future Enhancements

### Planned Features
- [ ] **Multi-language support** for document processing and chat interface
- [ ] **Advanced document preprocessing** with custom text cleaning and normalization
- [ ] **Custom embedding models** support for specialized domains
- [ ] **User authentication and sessions** with personal document collections
- [ ] **Document versioning** and change tracking
- [ ] **Advanced analytics dashboard** with usage statistics and insights
- [ ] **Export capabilities** for chat history and search results
- [ ] **Integration with cloud storage** (AWS S3, Google Drive, Dropbox)
- [ ] **Collaborative features** for team document sharing
- [ ] **Advanced search filters** by file type, date, and content type

### Technical Improvements
- [ ] **Streaming responses** for real-time chat experience
- [ ] **Background processing** for large document batches
- [ ] **Database integration** for persistent chat history and user data
- [ ] **Docker containerization** for easy deployment
- [ ] **Horizontal scaling** support for multiple users
- [ ] **Advanced chunking strategies** with overlap optimization
- [ ] **Vector store compression** for reduced storage requirements
- [ ] **API rate limiting** and usage monitoring
- [ ] **Enhanced error handling** with retry mechanisms
- [ ] **Performance monitoring** and optimization tools