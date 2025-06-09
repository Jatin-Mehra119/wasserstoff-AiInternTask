from pydantic import BaseModel
from typing import List, Dict, Any


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