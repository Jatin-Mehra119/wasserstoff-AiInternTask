import os
import base64
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import hashlib
from datetime import datetime

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

# Additional imports
from dotenv import load_dotenv
import re

from rag_elements.config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format=Config.LOG_FORMAT)
logger = logging.getLogger(__name__)

class EnhancedDocumentProcessor:
    """
    Enhanced document processor with citation tracking and theme analysis capabilities.
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """Initialize the Enhanced DocumentProcessor."""
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.warning("GROQ API key not found. Image OCR will not be available.")
            self.vision_llm = None
        else:
            self.vision_llm = ChatGroq(
                model=Config.VISION_LLM_MODEL,
                api_key=self.groq_api_key
            )
        
        # Initialize chat model for analysis
        self.chat_llm = ChatGroq(
            model=Config.CHAT_LLM_MODEL,
            api_key=self.groq_api_key
        ) if self.groq_api_key else None
        
        # Initialize embeddings
        self.embeddings = SentenceTransformerEmbeddings(model_name=Config.EMBEDDINGS_MODEL)
        
        # Initialize text splitter with better chunk tracking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap= Config.CHUNK_OVERLAP,
            length_function=len,
            separators= Config.CHUNK_SEPARATORS
        )
        
        # Document tracking
        self.document_metadata = {}
        self.processed_documents = []
        self.vector_store = None
        
        # Supported file extensions
        self.supported_extensions = {
            '.pdf': self._process_pdf,
            '.txt': self._process_text,
            '.md': self._process_text,
            '.py': self._process_text,
            '.js': self._process_text,
            '.html': self._process_text,
            '.csv': self._process_text,
            '.json': self._process_text,
            '.png': self._process_image,
            '.jpg': self._process_image,
            '.jpeg': self._process_image,
            '.bmp': self._process_image,
            '.tiff': self._process_image,
            '.webp': self._process_image
        }
    
    def _generate_chunk_id(self, content: str, source: str, chunk_index: int) -> str:
        """Generate a unique ID for a document chunk."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:Config.CONTENT_HASH_LENGTH]
        source_hash = hashlib.md5(source.encode()).hexdigest()[:Config.SOURCE_HASH_LENGTH]
        return f"{source_hash}_{chunk_index}_{content_hash}"
    
    def _extract_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """Extract sentences with their positions in the text."""
        sentences = []
        sentence_pattern = r'[.!?]+\s+'
        
        current_pos = 0
        for match in re.finditer(sentence_pattern, text):
            sentence = text[current_pos:match.end()].strip()
            if sentence:
                sentences.append((sentence, current_pos, match.end()))
            current_pos = match.end()
        
        # Add the last sentence if it doesn't end with punctuation
        if current_pos < len(text):
            remaining = text[current_pos:].strip()
            if remaining:
                sentences.append((remaining, current_pos, len(text)))
        
        return sentences
    
    def extract_text_from_image(self, img_path: str) -> str:
        """Extract text from image using OCR."""
        if not self.vision_llm:
            logger.error("Vision LLM not initialized. Please provide GROQ API key.")
            return ""
        
        try:
            with open(img_path, "rb") as image_file:
                image_bytes = image_file.read()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            message = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": (
                                Config.OCR_PROMPT if Config.OCR_PROMPT else
                                "Extract all the text from this image. "
                                "Preserve the structure and formatting as much as possible. "
                                "If there's no text, return 'No text found'."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ]
                )
            ]

            response = self.vision_llm.invoke(message)
            extracted_text = response.content.strip()
            
            if extracted_text.lower() == "no text found":
                return ""
            
            return extracted_text

        except Exception as e:
            logger.error(f"Error extracting text from {img_path}: {str(e)}")
            return ""
    
    def _process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF files with enhanced metadata."""
        documents = []
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            for page_num, page in enumerate(pages):
                if page.page_content.strip():
                    # Extract sentences for better citation tracking
                    sentences = self._extract_sentences(page.page_content)
                    
                    # Create enhanced metadata
                    metadata = {
                        "source": file_path,
                        "page": page_num + 1,
                        "type": "pdf",
                        "total_pages": len(pages),
                        "sentences": len(sentences),
                        "word_count": len(page.page_content.split()),
                        "processed_at": datetime.now().isoformat()
                    }
                    
                    documents.append(Document(
                        page_content=page.page_content,
                        metadata=metadata
                    ))
            
            logger.info(f"Processed PDF: {file_path} - {len(documents)} pages")
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
        
        return documents
    
    def _process_text(self, file_path: str) -> List[Document]:
        """Process text files with enhanced metadata."""
        documents = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if content.strip():
                sentences = self._extract_sentences(content)
                
                metadata = {
                    "source": file_path,
                    "type": "text",
                    "sentences": len(sentences),
                    "word_count": len(content.split()),
                    "char_count": len(content),
                    "processed_at": datetime.now().isoformat()
                }
                
                documents.append(Document(
                    page_content=content,
                    metadata=metadata
                ))
            
            logger.info(f"Processed text file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
        
        return documents
    
    def _process_image(self, file_path: str) -> List[Document]:
        """Process image files with OCR and enhanced metadata."""
        documents = []
        try:
            extracted_text = self.extract_text_from_image(file_path)
            
            if extracted_text:
                sentences = self._extract_sentences(extracted_text)
                
                metadata = {
                    "source": file_path,
                    "type": "image",
                    "sentences": len(sentences),
                    "word_count": len(extracted_text.split()),
                    "char_count": len(extracted_text),
                    "processed_at": datetime.now().isoformat()
                }
                
                documents.append(Document(
                    page_content=extracted_text,
                    metadata=metadata
                ))
                
                logger.info(f"Processed image: {file_path} - Extracted {len(extracted_text)} characters")
            else:
                logger.warning(f"No text extracted from image: {file_path}")
                
        except Exception as e:
            logger.error(f"Error processing image {file_path}: {str(e)}")
        
        return documents
    
    def process_files(self, file_paths: List[str]) -> List[Document]:
        """Process a list of file paths."""
        documents = []
        
        logger.info(f"Processing {len(file_paths)} files...")
        
        for file_path in file_paths:
            try:
                file_path_obj = Path(file_path)
                if not file_path_obj.exists():
                    logger.warning(f"File does not exist: {file_path}")
                    continue
                
                file_extension = file_path_obj.suffix.lower()
                if file_extension not in self.supported_extensions:
                    logger.warning(f"Unsupported file type: {file_extension} for file {file_path}")
                    continue
                
                processor_func = self.supported_extensions[file_extension]
                file_documents = processor_func(file_path)
                documents.extend(file_documents)
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
        
        logger.info(f"Successfully processed {len(documents)} documents from {len(file_paths)} files")
        return documents
    
    def process_directory(self, directory_path: str, recursive: bool = Config.ENABLE_RECURSIVE_DIRECTORY_PROCESSING) -> List[Document]:
        """Process all supported files in a directory."""
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return documents
        
        if recursive:
            files = directory.rglob("*")
        else:
            files = directory.glob("*")
        
        supported_files = [
            f for f in files 
            if f.is_file() and f.suffix.lower() in self.supported_extensions
        ]
        
        logger.info(f"Found {len(supported_files)} supported files in {directory_path}")
        
        for file_path in supported_files:
            try:
                file_extension = file_path.suffix.lower()
                processor_func = self.supported_extensions[file_extension]
                file_documents = processor_func(str(file_path))
                documents.extend(file_documents)
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
        
        logger.info(f"Successfully processed {len(documents)} documents from {len(supported_files)} files")
        return documents
    
    def create_enhanced_vector_store(self, documents: List[Document]) -> FAISS:
        """Create FAISS vector store with enhanced chunk metadata."""
        if not documents:
            logger.error("No documents provided for vector store creation")
            return None
        
        logger.info("Creating enhanced document chunks...")
        enhanced_chunks = []
        
        for doc in documents:
            # Split document into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            for i, chunk in enumerate(chunks):
                # Add enhanced metadata to each chunk
                chunk_id = self._generate_chunk_id(chunk.page_content, doc.metadata["source"], i)
                
                # Find sentence boundaries within the chunk
                sentences = self._extract_sentences(chunk.page_content)
                
                enhanced_metadata = {
                    **chunk.metadata,
                    "chunk_id": chunk_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "chunk_sentences": len(sentences),
                    "chunk_word_count": len(chunk.page_content.split()),
                    "start_char": i * (self.text_splitter._chunk_size - self.text_splitter._chunk_overlap),
                }
                
                # Create new document with enhanced metadata
                enhanced_chunk = Document(
                    page_content=chunk.page_content,
                    metadata=enhanced_metadata
                )
                enhanced_chunks.append(enhanced_chunk)
        
        logger.info(f"Created {len(enhanced_chunks)} enhanced document chunks")
        
        # Create vector store
        logger.info("Creating FAISS vector store...")
        vector_store = FAISS.from_documents(enhanced_chunks, self.embeddings)
        
        self.vector_store = vector_store
        self.processed_documents = documents
        
        logger.info(f"Successfully created FAISS vector store with {len(enhanced_chunks)} chunks")
        return vector_store
    
    def search_with_citations(self, query: str, k: int = Config.DEFAULT_SEARCH_K) -> List[Dict[str, Any]]:
        """Search for similar documents and return results with citation information."""
        if not self.vector_store:
            logger.error("No vector store available. Create or load one first.")
            return []
        
        try:
            # Get similar documents
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            citation_results = []
            for doc, score in results:
                citation_info = {
                    "content": doc.page_content,
                    "score": float(score),
                    "source": doc.metadata.get("source", "Unknown"),
                    "type": doc.metadata.get("type", "Unknown"),
                    "chunk_id": doc.metadata.get("chunk_id", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", 0),
                    "page": doc.metadata.get("page", None),
                    "word_count": doc.metadata.get("chunk_word_count", 0),
                    "sentences": doc.metadata.get("chunk_sentences", 0),
                    "processed_at": doc.metadata.get("processed_at", "Unknown")
                }
                
                # Add specific citation format based on document type
                if doc.metadata.get("type") == "pdf" and doc.metadata.get("page"):
                    citation_info["citation"] = f"{Path(doc.metadata['source']).name}, Page {doc.metadata['page']}"
                elif doc.metadata.get("type") == "text":
                    citation_info["citation"] = f"{Path(doc.metadata['source']).name}, Chunk {doc.metadata.get('chunk_index', 0) + 1}"
                elif doc.metadata.get("type") == "image_ocr":
                    citation_info["citation"] = f"{Path(doc.metadata['source']).name} (OCR)"
                else:
                    citation_info["citation"] = f"{Path(doc.metadata['source']).name}"
                
                citation_results.append(citation_info)
            
            logger.info(f"Found {len(citation_results)} results with citations for query: '{query}'")
            return citation_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def analyze_themes(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze common themes across search results."""
        if not self.chat_llm or not search_results:
            return {"themes": [], "summary": "Unable to analyze themes"}
        
        try:
            # Prepare content for theme analysis
            contents = [result["content"] for result in search_results]
            combined_content = "\n\n---\n\n".join(contents)
            
            theme_analysis_prompt = Config.THEME_ANALYSIS_PROMPT_TEMPLATE.format(
                query=query,
                content=combined_content[:Config.MAX_CONTENT_LENGTH_FOR_THEME_ANALYSIS]
            )
            
            response = self.chat_llm.invoke(theme_analysis_prompt)
            
            # Try to parse JSON response
            try:
                import json
                theme_data = json.loads(response.content)
                return theme_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "themes": [{"name": "Analysis Available", "description": response.content[:200], "frequency": "varies"}],
                    "summary": response.content,
                    "insights": ["Theme analysis completed"]
                }
            
        except Exception as e:
            logger.error(f"Error analyzing themes: {str(e)}")
            return {
                "themes": [{"name": "Error", "description": f"Theme analysis failed: {str(e)}", "frequency": "N/A"}],
                "summary": "Unable to analyze themes due to an error",
                "insights": []
            }
    
    def save_vector_store(self, save_path: str):
        """Save the FAISS vector store with enhanced metadata."""
        if not self.vector_store:
            logger.error("No vector store to save. Create one first.")
            return
        
        try:
            self.vector_store.save_local(save_path)
            
            # Save enhanced metadata
            metadata = {
                "num_documents": len(self.processed_documents),
                "num_chunks": self.vector_store.index.ntotal,
                "embedding_model": Config.EMBEDDINGS_MODEL,
                "processed_files": [
                    {
                        "source": doc.metadata.get("source", ""),
                        "type": doc.metadata.get("type", ""),
                        "word_count": doc.metadata.get("word_count", 0),
                        "processed_at": doc.metadata.get("processed_at", "")
                    } for doc in self.processed_documents
                ],
                "created_at": datetime.now().isoformat(),
                "chunk_size": self.text_splitter._chunk_size,
                "chunk_overlap": self.text_splitter._chunk_overlap
            }
            
            with open(f"{save_path}/{Config.ENHANCED_METADATA_FILENAME}", "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Enhanced vector store saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
    
    def load_vector_store(self, load_path: str) -> FAISS:
        """Load a FAISS vector store from disk."""
        try:
            vector_store = FAISS.load_local(
                load_path, 
                self.embeddings, 
                allow_dangerous_deserialization=Config.ENABLE_DANGEROUS_DESERIALIZATION
            )
            self.vector_store = vector_store
            
            # Load enhanced metadata if available
            metadata_path = f"{load_path}/{Config.ENHANCED_METADATA_FILENAME}"
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                logger.info(f"Loaded enhanced vector store with {metadata.get('num_chunks', 'unknown')} chunks")
            
            logger.info(f"Vector store loaded from {load_path}")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
