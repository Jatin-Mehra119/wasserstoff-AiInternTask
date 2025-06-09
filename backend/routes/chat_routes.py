import os
import sys
from fastapi import APIRouter, HTTPException
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import ChatMessage, ChatResponse
from utils import get_processor, generate_response, get_global_state, update_global_state

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message and return response with citations and themes."""
    try:
        processor = get_processor()
        state = get_global_state()
        
        if not state["vector_store_loaded"]:
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
        current_history = state["chat_history"]
        current_history.append({
            "user_message": message.message,
            "assistant_response": chat_response.dict(),
            "timestamp": datetime.now().isoformat()
        })
        
        update_global_state(chat_history=current_history)
        
        return chat_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/clear-chat")
async def clear_chat():
    """Clear chat history and reset session data."""
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils import clear_session_data
    
    clear_session_data()
    
    return {"status": "success", "message": "Chat history and session data cleared"}
