# Configuration file for Enhanced Vector Database
# This file contains all configurable parameters for the EnhancedDocumentProcessor

# Model Configuration
class Config: 
    # Model Names
    CHAT_LLM_MODEL = "llama-3.3-70b-versatile"
    VISION_LLM_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
    EMBEDDINGS_MODEL = "all-MiniLM-L6-v2"

    # Text Splitting Configuration
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    CHUNK_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

    # Search Configuration
    DEFAULT_SEARCH_K = 5

    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    # Hash Configuration
    CONTENT_HASH_LENGTH = 8
    SOURCE_HASH_LENGTH = 8

    # OCR Configuration
    OCR_PROMPT = (
        "Extract all the text from this image. "
        "Preserve the structure and formatting as much as possible. "
        "If there's no text, return 'No text found'."
    )

    # Theme Analysis Configuration
    THEME_ANALYSIS_PROMPT_TEMPLATE = """
    Analyze the following document excerpts and identify common themes related to the query: "{query}"

    Document excerpts:
    {content}

    Please provide:
    1. A list of 3-5 main themes/topics that appear across these documents
    2. A brief summary of how these themes relate to the query
    3. Key insights or patterns you notice

    Format your response as JSON with the following structure:
    {{
        "themes": [
            {{"name": "Theme Name", "description": "Brief description", "frequency": "how often it appears"}},
            ...
        ],
        "summary": "Overall summary of themes",
        "insights": ["Key insight 1", "Key insight 2", ...]
    }}
    """

    # File Processing Configuration
    ENABLE_RECURSIVE_DIRECTORY_PROCESSING = True
    MAX_CONTENT_LENGTH_FOR_THEME_ANALYSIS = 10000

    # Metadata Configuration
    ENHANCED_METADATA_FILENAME = "enhanced_metadata.json"

    # Error Handling Configuration
    ENABLE_DANGEROUS_DESERIALIZATION = True
