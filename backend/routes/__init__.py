import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from .main_routes import router as main_router
from .upload_routes import router as upload_router
from .chat_routes import router as chat_router
from .store_routes import router as store_router

__all__ = ["main_router", "upload_router", "chat_router", "store_router"]
