# Development Guide

This guide helps developers understand the codebase and contribute to the RAG Chat Application.

## 🏗️ Project Structure

```
wasserstoff-AiInternTask/
├── rag_elements/              # 🧠 Core RAG Engine
│   ├── enhanced_vectordb.py   # Main RAG implementation
│   └── config.py              # Configuration management
├── backend/                   # 🚀 FastAPI Production Server
│   ├── main.py               # App entry point
│   ├── models.py             # Pydantic schemas
│   ├── utils.py              # Utilities and state
│   └── routes/               # API endpoints
├── frontend/                  # 🎨 Web Interface
│   ├── index.html            # Main UI
│   ├── style.css             # Styling
│   └── script.js             # Frontend logic
├── tests/                     # 🧪 Test Suite
└── docs/                      # 📚 Documentation
```

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Text editor/IDE (VS Code recommended)

### Environment Setup
```bash
# Clone repository
git clone https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask.git
cd wasserstoff-AiInternTask

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r tests/requirements-test.txt

# Set up environment variables
cp .env.example .env  # Create if exists
# Add your GROQ_API_KEY to .env
```

### Running in Development Mode
```bash
# Start FastAPI with hot reload
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run Streamlit version
streamlit run streamlit_rag_app.py
```

## 🧱 Core Components

### 1. RAG Engine (`rag_elements/enhanced_vectordb.py`)

The heart of the application. Key classes and methods:

```python
class EnhancedDocumentProcessor:
    def process_files(self, file_paths)              # Multi-format processing
    def create_enhanced_vector_store(self, documents) # FAISS index creation
    def search_with_citations(self, query, k=5)      # Semantic search
    def get_chat_response(self, query)                # End-to-end chat
    def save_vector_store(self, path)                 # Persistence
    def load_vector_store(self, path)                 # Restore data
```

### 2. FastAPI Backend (`backend/`)

**Entry Point (`main.py`)**:
- FastAPI app initialization
- CORS configuration
- Route registration

**Data Models (`models.py`)**:
- Pydantic schemas for API requests/responses
- Type validation and serialization

**Routes (`routes/`)**:
- `main_routes.py` - Frontend serving, health checks
- `upload_routes.py` - File upload and processing
- `chat_routes.py` - Chat interface and AI responses
- `store_routes.py` - Vector store management

**Utilities (`utils.py`)**:
- Global state management
- Helper functions
- Error handling utilities

### 3. Frontend (`frontend/`)

Modern web interface with:
- **HTML**: Semantic structure with responsive layout
- **CSS**: Modern styling with CSS Grid/Flexbox
- **JavaScript**: Async API calls, real-time updates, file handling

## 🔄 Data Flow

### Document Processing Pipeline
1. **File Upload** → `upload_routes.py`
2. **Text Extraction** → `enhanced_vectordb.py`
3. **Chunking** → LangChain text splitters
4. **Embeddings** → Sentence Transformers
5. **Indexing** → FAISS vector store
6. **Metadata Storage** → JSON persistence

### Chat Pipeline
1. **User Query** → `chat_routes.py`
2. **Semantic Search** → FAISS similarity search
3. **Context Retrieval** → Top-K document chunks
4. **AI Response** → GROQ API integration
5. **Citation Generation** → Source attribution
6. **Response Formatting** → Markdown output

## 🧪 Testing

### Running Tests
```bash
cd tests

# Run all tests
bash run_tests.sh

# Run specific test files
python -m pytest test_endpoints_pytest.py -v
python test_api_endpoints.py
```

### Test Structure
- `test_api_endpoints.py` - Basic API endpoint testing
- `test_endpoints_pytest.py` - Comprehensive pytest suite
- `run_tests.sh` - Test runner script

### Writing Tests
Follow these patterns:

```python
# API endpoint test
def test_upload_endpoint():
    response = requests.post(f"{BASE_URL}/upload-files", files=files)
    assert response.status_code == 200
    assert "total_files" in response.json()

# Pytest test
@pytest.mark.asyncio
async def test_chat_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/chat", 
                                   json={"message": "test"})
        assert response.status_code == 200
```

## 🔌 Adding New Features

### Adding a New API Endpoint

1. **Define Pydantic Model** (`models.py`):
```python
class NewFeatureRequest(BaseModel):
    parameter: str
    optional_param: Optional[int] = None

class NewFeatureResponse(BaseModel):
    result: str
    success: bool
```

2. **Create Route Handler** (`routes/new_routes.py`):
```python
from fastapi import APIRouter, HTTPException
from ..models import NewFeatureRequest, NewFeatureResponse

router = APIRouter()

@router.post("/new-feature", response_model=NewFeatureResponse)
async def new_feature_endpoint(request: NewFeatureRequest):
    try:
        # Implementation here
        return NewFeatureResponse(result="success", success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

3. **Register Router** (`main.py`):
```python
from .routes.new_routes import router as new_router
app.include_router(new_router)
```

4. **Add Frontend Integration** (`frontend/script.js`):
```javascript
async function callNewFeature(data) {
    const response = await fetch('/new-feature', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return response.json();
}
```

### Extending the RAG Engine

To add new document types or processing capabilities:

1. **Add File Type Support** (`enhanced_vectordb.py`):
```python
def extract_text_from_new_format(self, file_path):
    # Implement extraction logic
    return extracted_text

def process_files(self, file_paths):
    for file_path in file_paths:
        if file_path.endswith('.new_format'):
            text = self.extract_text_from_new_format(file_path)
            # Process text...
```

2. **Update Frontend File Acceptance** (`index.html`):
```html
<input type="file" accept=".pdf,.txt,.new_format" multiple>
```

## 🎨 Frontend Development

### Key JavaScript Functions
- `uploadFiles()` - Handle file uploads with progress
- `sendMessage()` - Send chat messages and display responses
- `updateStats()` - Refresh processing statistics
- `displayCitations()` - Show document sources

### CSS Architecture
- Mobile-first responsive design
- CSS custom properties for theming
- Flexbox/Grid layouts
- Component-based styling

### Adding UI Components
1. Add HTML structure
2. Style with CSS classes
3. Add JavaScript event handlers
4. Connect to backend APIs

## 🐛 Debugging

### Common Issues

**CORS Errors**:
- Check `main.py` CORS configuration
- Ensure frontend runs on allowed origins

**Import Errors**:
- Verify Python path and virtual environment
- Check `requirements.txt` dependencies

**API Key Issues**:
- Confirm GROQ API key is set
- Check environment variable loading

### Logging

Add logging to your code:
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/endpoint")
async def endpoint():
    logger.info("Processing request")
    try:
        # Logic here
        logger.debug("Success")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

## 📝 Code Style Guidelines

### Python
- Follow PEP 8
- Use type hints
- Add docstrings
- Maximum line length: 88 characters

```python
def process_document(file_path: str, options: Dict[str, Any]) -> ProcessResult:
    """
    Process a document and extract text content.
    
    Args:
        file_path: Path to the document file
        options: Processing configuration options
        
    Returns:
        ProcessResult containing extracted text and metadata
        
    Raises:
        ProcessingError: If document cannot be processed
    """
    # Implementation...
```

### JavaScript
- Use modern ES6+ syntax
- Prefer `const`/`let` over `var`
- Use async/await for promises
- Add JSDoc comments

```javascript
/**
 * Upload files to the server
 * @param {FileList} files - Files to upload
 * @returns {Promise<Object>} Upload result
 */
async function uploadFiles(files) {
    // Implementation...
}
```

## 🚀 Deployment

### Development
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (if configured)
```bash
docker build -t rag-chat-app .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key rag-chat-app
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Ensure tests pass: `bash tests/run_tests.sh`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FAISS Documentation](https://faiss.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [GROQ API Documentation](https://console.groq.com/docs)
