from fastapi import FastAPI, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import sys
import tempfile
import shutil
import json
import asyncio
import aiofiles
from pathlib import Path
from datetime import datetime
import uuid

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rag_elements.enhanced_vectordb import EnhancedDocumentProcessor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Agentic RAG Chat API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Global processor instance
processor_instance = None
vector_store_loaded = False
processing_stats = {}
chat_history = []

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    citations: List[Dict[str, Any]]
    themes: Dict[str, Any]
    timestamp: str

class ProcessingStats(BaseModel):
    total_files: int
    total_documents: int
    total_chunks: int
    file_types: List[str]
    type_counts: Dict[str, int]
    processed_at: str

class APIKeyRequest(BaseModel):
    api_key: str

# Helper functions
def initialize_processor(groq_api_key: str = None):
    """Initialize the document processor."""
    global processor_instance
    
    api_key = groq_api_key or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="GROQ API key is required")
    
    processor_instance = EnhancedDocumentProcessor(api_key)
    return processor_instance

def get_processor():
    """Get the processor instance."""
    global processor_instance
    if not processor_instance:
        initialize_processor()
    return processor_instance

async def save_uploaded_file(upload_file: UploadFile, temp_dir: str) -> str:
    """Save an uploaded file to temporary directory."""
    file_path = os.path.join(temp_dir, upload_file.filename)
    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    return file_path

# API Routes

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    return FileResponse(frontend_path)

@app.post("/api/set-api-key")
async def set_api_key(request: APIKeyRequest):
    """Set the GROQ API key."""
    try:
        initialize_processor(request.api_key)
        return {"status": "success", "message": "API key set successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process multiple files."""
    global vector_store_loaded, processing_stats
    
    try:
        processor = get_processor()
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        temp_files = []
        
        # Save uploaded files
        for file in files:
            if file.filename:
                file_path = await save_uploaded_file(file, temp_dir)
                temp_files.append(file_path)
        
        # Process files
        documents = processor.process_files(temp_files)
        
        if documents:
            # Create vector store
            vector_store = processor.create_enhanced_vector_store(documents)
            
            if vector_store:
                vector_store_loaded = True
                
                # Calculate statistics
                original_files = {}
                file_type_counts = {}
                total_chunks = vector_store.index.ntotal
                
                for doc in documents:
                    source_file = doc.metadata.get("source", "unknown")
                    doc_type = doc.metadata.get("type", "unknown")
                    
                    if source_file not in original_files:
                        original_files[source_file] = doc_type
                        file_type_counts[doc_type] = file_type_counts.get(doc_type, 0) + 1
                
                processing_stats = {
                    "total_files": len(original_files),
                    "total_documents": len(documents),
                    "total_chunks": total_chunks,
                    "file_types": list(file_type_counts.keys()),
                    "type_counts": file_type_counts,
                    "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Clean up temp files
                shutil.rmtree(temp_dir)
                
                return {
                    "status": "success",
                    "message": f"Successfully processed {len(original_files)} files",
                    "stats": processing_stats
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to create vector store")
        else:
            raise HTTPException(status_code=400, detail="No documents were processed successfully")
            
    except Exception as e:
        # Clean up temp files in case of error
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-directory")
async def process_directory(directory_path: str = Form(...)):
    """Process documents from a directory."""
    global vector_store_loaded, processing_stats
    
    try:
        processor = get_processor()
        
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=400, detail=f"Directory does not exist: {directory_path}")
        
        documents = processor.process_directory(directory_path, recursive=True)
        
        if documents:
            vector_store = processor.create_enhanced_vector_store(documents)
            
            if vector_store:
                vector_store_loaded = True
                
                # Calculate statistics
                original_files = {}
                file_type_counts = {}
                total_chunks = vector_store.index.ntotal
                
                for doc in documents:
                    source_file = doc.metadata.get("source", "unknown")
                    doc_type = doc.metadata.get("type", "unknown")
                    
                    if source_file not in original_files:
                        original_files[source_file] = doc_type
                        file_type_counts[doc_type] = file_type_counts.get(doc_type, 0) + 1
                
                processing_stats = {
                    "total_files": len(original_files),
                    "total_documents": len(documents),
                    "total_chunks": total_chunks,
                    "file_types": list(file_type_counts.keys()),
                    "type_counts": file_type_counts,
                    "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                return {
                    "status": "success",
                    "message": f"Successfully processed {len(original_files)} files from directory",
                    "stats": processing_stats
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to create vector store")
        else:
            raise HTTPException(status_code=400, detail="No documents found or processed in the directory")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message and return response with citations and themes."""
    global chat_history
    
    try:
        processor = get_processor()
        
        if not vector_store_loaded:
            raise HTTPException(status_code=400, detail="No vector store loaded. Please upload and process documents first.")
        
        # Search for relevant documents
        search_results = processor.search_with_citations(message.message, k=5)
        
        if not search_results:
            response_text = "I couldn't find any relevant information in the documents for your query."
            chat_response = ChatResponse(
                response=response_text,
                citations=[],
                themes={},
                timestamp=datetime.now().isoformat()
            )
        else:
            # Analyze themes
            theme_analysis = processor.analyze_themes(message.message, search_results)
            
            # Generate response
            response_text = generate_response(processor, message.message, search_results, theme_analysis)
            
            chat_response = ChatResponse(
                response=response_text,
                citations=search_results,
                themes=theme_analysis,
                timestamp=datetime.now().isoformat()
            )
        
        # Add to chat history
        chat_history.append({
            "user_message": message.message,
            "assistant_response": chat_response.dict(),
            "timestamp": datetime.now().isoformat()
        })
        
        return chat_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_response(processor, query: str, search_results: List[Dict], theme_analysis: Dict) -> str:
    """Generate a comprehensive response based on search results and theme analysis."""
    if not processor.chat_llm:
        # Fallback response without LLM
        response_parts = [
            f"Based on your query '{query}', I found {len(search_results)} relevant document sections.",
            "\n**Key Information:**"
        ]
        
        for i, result in enumerate(search_results[:3], 1):
            content_preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
            response_parts.append(f"\n{i}. From {result['citation']}: {content_preview}")
        
        return "\n".join(response_parts)
    
    try:
        # Use LLM to generate comprehensive response
        context_content = "\n\n".join([f"Document {i+1} ({result['citation']}):\n{result['content']}" 
                                     for i, result in enumerate(search_results)])
        
        response_prompt = f"""
        Based on the following document excerpts, provide a comprehensive answer to the user's query: "{query}"
        
        Document excerpts:
        {context_content}
        
        Please provide:
        1. A direct answer to the user's question
        2. Key points from the documents
        3. Any relevant details or context
        4. Connections between different sources if applicable
        
        Make sure to reference the information from the documents and provide a helpful, accurate response.
        """
        
        llm_response = processor.chat_llm.invoke(response_prompt)
        return llm_response.content
        
    except Exception as e:
        # Fallback to simple response
        return f"Based on your query '{query}', I found relevant information in {len(search_results)} document sections. Please see the citations below for detailed information."

@app.get("/api/stats")
async def get_stats():
    """Get processing statistics."""
    return {"stats": processing_stats, "vector_store_loaded": vector_store_loaded}

@app.get("/api/chat-history")
async def get_chat_history():
    """Get chat history."""
    return {"history": chat_history}

@app.post("/api/save-vector-store")
async def save_vector_store():
    """Save the current vector store."""
    try:
        processor = get_processor()
        
        if not processor.vector_store:
            raise HTTPException(status_code=400, detail="No vector store to save. Process documents first.")
        
        save_path = "vector_store"
        processor.save_vector_store(save_path)
        
        return {"status": "success", "message": "Vector store saved successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/load-vector-store")
async def load_vector_store():
    """Load a previously saved vector store."""
    global vector_store_loaded, processing_stats
    
    try:
        processor = get_processor()
        
        load_path = "vector_store"
        vector_store = processor.load_vector_store(load_path)
        
        if vector_store:
            vector_store_loaded = True
            
            # Load metadata if available
            metadata_path = f"{load_path}/enhanced_metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                processed_files = metadata.get("processed_files", [])
                unique_files = len(set(f.get("source", "") for f in processed_files))
                
                processing_stats = {
                    "total_files": unique_files,
                    "total_documents": metadata.get("num_documents", 0),
                    "total_chunks": metadata.get("num_chunks", 0),
                    "file_types": list(set(f["type"] for f in processed_files if "type" in f)),
                    "processed_at": metadata.get("created_at", "Unknown")
                }
            
            return {"status": "success", "message": "Vector store loaded successfully", "stats": processing_stats}
        else:
            raise HTTPException(status_code=400, detail="Failed to load vector store. Check if it exists.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/clear-chat")
async def clear_chat():
    """Clear chat history."""
    global chat_history
    chat_history = []
    return {"status": "success", "message": "Chat history cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
