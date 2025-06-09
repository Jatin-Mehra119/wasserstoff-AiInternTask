import os
import sys
import tempfile
import shutil
import json
import aiofiles
from fastapi import HTTPException, UploadFile
from typing import List, Dict
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rag_elements.enhanced_vectordb import EnhancedDocumentProcessor

# Global variables
processor_instance = None
vector_store_loaded = False
processing_stats = {}
chat_history = []


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


def calculate_processing_stats(documents, vector_store):
    """Calculate processing statistics from documents and vector store."""
    original_files = {}
    file_type_counts = {}
    total_chunks = vector_store.index.ntotal
    
    for doc in documents:
        source_file = doc.metadata.get("source", "unknown")
        doc_type = doc.metadata.get("type", "unknown")
        
        if source_file not in original_files:
            original_files[source_file] = doc_type
            file_type_counts[doc_type] = file_type_counts.get(doc_type, 0) + 1
    
    return {
        "total_files": len(original_files),
        "total_documents": len(documents),
        "total_chunks": total_chunks,
        "file_types": list(file_type_counts.keys()),
        "type_counts": file_type_counts,
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


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


def get_global_state():
    """Get the current global state."""
    return {
        "vector_store_loaded": vector_store_loaded,
        "processing_stats": processing_stats,
        "chat_history": chat_history,
        "processor_instance": processor_instance
    }


def update_global_state(**kwargs):
    """Update global state variables."""
    global vector_store_loaded, processing_stats, chat_history, processor_instance
    
    if "vector_store_loaded" in kwargs:
        vector_store_loaded = kwargs["vector_store_loaded"]
    if "processing_stats" in kwargs:
        processing_stats = kwargs["processing_stats"]
    if "chat_history" in kwargs:
        chat_history = kwargs["chat_history"]
    if "processor_instance" in kwargs:
        processor_instance = kwargs["processor_instance"]


def clear_session_data():
    """Clear all session data."""
    global chat_history, vector_store_loaded, processing_stats, processor_instance
    
    chat_history = []
    vector_store_loaded = False
    processing_stats = {}
    
    if processor_instance and processor_instance.vector_store:
        processor_instance.vector_store = None
