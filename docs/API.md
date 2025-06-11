# API Documentation

This document provides a quick reference for the RAG Chat Application REST API endpoints.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require a GROQ API key to be configured:

```bash
POST /set-api-key
Content-Type: application/json

{
  "api_key": "your_groq_api_key_here"
}
```

## Core Endpoints

### Document Processing

#### Upload Files
```bash
POST /upload-files
Content-Type: multipart/form-data

# Form data with file uploads
files: [file1.pdf, file2.txt, ...]
```

**Response:**
```json
{
  "total_files": 5,
  "total_documents": 12,
  "total_chunks": 87,
  "file_types": ["pdf", "txt", "py"],
  "type_counts": {"pdf": 3, "txt": 1, "py": 1}
}
```

#### Process Directory
```bash
POST /process-directory
Content-Type: application/x-www-form-urlencoded

directory_path=/path/to/documents
```

### Chat Interface

#### Send Chat Message
```bash
POST /chat
Content-Type: application/json

{
  "message": "What is the main topic of the documents?"
}
```

**Response:**
```json
{
  "response": "Based on the documents, the main topics include...",
  "citations": [
    {
      "content": "relevant excerpt from document",
      "citation": "/path/to/source/file.pdf",
      "type": "pdf",
      "score": 0.85
    }
  ],
  "themes": {
    "key_themes": ["AI", "Machine Learning", "RAG"],
    "analysis": "The documents focus on AI and ML concepts..."
  },
  "timestamp": "2025-06-11T10:30:00.123456"
}
```

### Data Management

#### Get Statistics
```bash
GET /stats
```

**Response:**
```json
{
  "total_files": 10,
  "total_documents": 25,
  "total_chunks": 150,
  "file_types": ["pdf", "txt", "py", "md"],
  "type_counts": {"pdf": 5, "txt": 3, "py": 1, "md": 1},
  "processed_at": "2025-06-11 10:30:00"
}
```

#### Get Chat History
```bash
GET /chat-history
```

**Response:**
```json
[
  {
    "user_message": "What is RAG?",
    "assistant_response": "RAG stands for Retrieval-Augmented Generation...",
    "timestamp": "2025-06-11T10:30:00.123456",
    "citations": [...]
  }
]
```

#### Clear Chat History
```bash
DELETE /clear-chat
```

### Vector Store Management

#### Save Vector Store
```bash
POST /save-vector-store
```

**Response:**
```json
{
  "message": "Vector store saved successfully"
}
```

#### Load Vector Store
```bash
POST /load-vector-store
```

**Response:**
```json
{
  "message": "Vector store loaded successfully",
  "stats": {
    "total_files": 10,
    "total_documents": 25,
    "total_chunks": 150
  }
}
```

## Frontend Serving

#### Main Application
```bash
GET /
```
Returns the HTML frontend application.

## Error Responses

All endpoints return errors in this format:
```json
{
  "detail": "Error description message"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid input)
- `422` - Validation Error
- `500` - Internal Server Error

## Interactive Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Examples

### Complete Workflow
```bash
# 1. Set API key
curl -X POST "http://localhost:8000/set-api-key" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "your_groq_key"}'

# 2. Upload files
curl -X POST "http://localhost:8000/upload-files" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"

# 3. Chat with documents
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarize the key points"}'

# 4. Get statistics
curl -X GET "http://localhost:8000/stats"

# 5. Save vector store
curl -X POST "http://localhost:8000/save-vector-store"
```

### Python Client Example
```python
import requests

base_url = "http://localhost:8000"

# Set API key
response = requests.post(f"{base_url}/set-api-key", 
                        json={"api_key": "your_groq_key"})

# Upload files
files = {'files': open('document.pdf', 'rb')}
response = requests.post(f"{base_url}/upload-files", files=files)

# Chat
response = requests.post(f"{base_url}/chat", 
                        json={"message": "What is this document about?"})
print(response.json())
```
