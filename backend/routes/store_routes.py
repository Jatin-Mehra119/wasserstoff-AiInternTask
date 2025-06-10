import os
import sys
import json
from fastapi import APIRouter, HTTPException

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import get_processor, get_global_state, update_global_state

router = APIRouter()


@router.post("/save-vector-store")
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


@router.post("/load-vector-store")
async def load_vector_store():
    """Load a previously saved vector store."""
    try:
        processor = get_processor()
        
        load_path = "vector_store"
        vector_store = processor.load_vector_store(load_path)
        
        if vector_store:
            # Load metadata if available
            metadata_path = f"{load_path}/enhanced_metadata.json"
            stats = {}
            
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                processed_files = metadata.get("processed_files", [])
                unique_files = len(set(f.get("source", "") for f in processed_files))
                
                stats = {
                    "total_files": unique_files,
                    "total_documents": metadata.get("num_documents", 0),
                    "total_chunks": metadata.get("num_chunks", 0),
                    "file_types": list(set(f["type"] for f in processed_files if "type" in f)),
                    "processed_at": metadata.get("created_at", "Unknown")
                }
            
            # Update global state
            update_global_state(
                vector_store_loaded=True,
                processing_stats=stats
            )
            
            return {"status": "success", "message": "Vector store loaded successfully", "stats": stats}
        else:
            raise HTTPException(status_code=400, detail="Failed to load vector store. Check if it exists.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
