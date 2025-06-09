import os
import sys
import tempfile
import shutil
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import List

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import (
    get_processor, save_uploaded_file, calculate_processing_stats,
    update_global_state, get_global_state
)

router = APIRouter()


@router.post("/api/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and process multiple files."""
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
                # Calculate statistics
                stats = calculate_processing_stats(documents, vector_store)
                
                # Update global state
                update_global_state(
                    vector_store_loaded=True,
                    processing_stats=stats
                )
                
                # Clean up temp files
                shutil.rmtree(temp_dir)
                
                return {
                    "status": "success",
                    "message": f"Successfully processed {stats['total_files']} files",
                    "stats": stats
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


@router.post("/api/process-directory")
async def process_directory(directory_path: str = Form(...)):
    """Process documents from a directory."""
    try:
        processor = get_processor()
        
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=400, detail=f"Directory does not exist: {directory_path}")
        
        documents = processor.process_directory(directory_path, recursive=True)
        
        if documents:
            vector_store = processor.create_enhanced_vector_store(documents)
            
            if vector_store:
                # Calculate statistics
                stats = calculate_processing_stats(documents, vector_store)
                
                # Update global state
                update_global_state(
                    vector_store_loaded=True,
                    processing_stats=stats
                )
                
                return {
                    "status": "success",
                    "message": f"Successfully processed {stats['total_files']} files from directory",
                    "stats": stats
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to create vector store")
        else:
            raise HTTPException(status_code=400, detail="No documents found or processed in the directory")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
