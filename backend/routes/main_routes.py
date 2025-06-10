import os
import sys
from fastapi import APIRouter
from fastapi.responses import FileResponse

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import APIKeyRequest
from utils import initialize_processor, get_global_state

router = APIRouter()


@router.get("/")
async def read_root():
    """Serve the main HTML page."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html")
    return FileResponse(frontend_path)


@router.post("/set-api-key")
async def set_api_key(request: APIKeyRequest):
    """Set the GROQ API key."""
    try:
        initialize_processor(request.api_key)
        return {"status": "success", "message": "API key set successfully"}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get processing statistics."""
    state = get_global_state()
    return {"stats": state["processing_stats"], "vector_store_loaded": state["vector_store_loaded"]}


@router.get("/chat-history")
async def get_chat_history():
    """Get chat history."""
    state = get_global_state()
    return {"history": state["chat_history"]}
