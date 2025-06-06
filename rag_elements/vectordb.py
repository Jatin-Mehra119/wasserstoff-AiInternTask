import os
import base64
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.schema.messages import HumanMessage

# Additional imports
import PyPDF2
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    A comprehensive document processor that can handle PDFs, images (with OCR), 
    and text files to create a FAISS vector database compatible with LangChain agents.
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the DocumentProcessor.
        
        Args:
            groq_api_key: Optional GROQ API key. If not provided, will look for GROQ_API_KEY env var.
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.warning("GROQ API key not found. Image OCR will not be available.")
            self.vision_llm = None
        else:
            self.vision_llm = ChatGroq(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                api_key=self.groq_api_key
            )
        
        # Initialize embeddings
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
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
        
        self.processed_documents = []
        self.vector_store = None
    
    def extract_text_from_image(self, img_path: str) -> str:
        """
        Extract text from an image file using a multimodal model.
        
        Args:
            img_path: Path to the image file
            
        Returns:
            Extracted text from the image
        """
        if not self.vision_llm:
            logger.error("Vision LLM not initialized. Please provide GROQ API key.")
            return ""
        
        try:
            # Read image and encode as base64
            with open(img_path, "rb") as image_file:
                image_bytes = image_file.read()

            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            # Prepare the prompt including the base64 image data
            message = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": (
                                "Extract all the text from this image. "
                                "Return only the extracted text, no explanations. "
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

            # Call the vision-capable model
            response = self.vision_llm.invoke(message)
            extracted_text = response.content.strip()
            
            if extracted_text.lower() == "no text found":
                return ""
            
            return extracted_text

        except Exception as e:
            error_msg = f"Error extracting text from {img_path}: {str(e)}"
            logger.error(error_msg)
            return ""
    
    def _process_pdf(self, file_path: str) -> List[Document]:
        """Process PDF files and extract text."""
        documents = []
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            for page in pages:
                if page.page_content.strip():
                    documents.append(Document(
                        page_content=page.page_content,
                        metadata={
                            "source": file_path,
                            "page": page.metadata.get("page", 0),
                            "type": "pdf"
                        }
                    ))
            
            logger.info(f"Processed PDF: {file_path} - {len(documents)} pages")
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
        
        return documents
    
    def _process_text(self, file_path: str) -> List[Document]:
        """Process text files."""
        documents = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if content.strip():
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "type": "text"
                    }
                ))
            
            logger.info(f"Processed text file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
        
        return documents
    
    def _process_image(self, file_path: str) -> List[Document]:
        """Process image files using OCR."""
        documents = []
        try:
            extracted_text = self.extract_text_from_image(file_path)
            
            if extracted_text:
                documents.append(Document(
                    page_content=extracted_text,
                    metadata={
                        "source": file_path,
                        "type": "image_ocr"
                    }
                ))
                logger.info(f"Processed image: {file_path} - Extracted {len(extracted_text)} characters")
            else:
                logger.warning(f"No text extracted from image: {file_path}")
                
        except Exception as e:
            logger.error(f"Error processing image {file_path}: {str(e)}")
        
        return documents
    
    def process_directory(self, directory_path: str, recursive: bool = True) -> List[Document]:
        """
        Process all supported files in a directory.
        
        Args:
            directory_path: Path to the directory containing documents
            recursive: Whether to search subdirectories recursively
            
        Returns:
            List of processed documents
        """
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return documents
        
        # Get all files
        if recursive:
            files = directory.rglob("*")
        else:
            files = directory.glob("*")
        
        # Filter for supported file types
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
    
    def process_files(self, file_paths: List[str]) -> List[Document]:
        """
        Process a list of specific files.
        
        Args:
            file_paths: List of file paths to process
            
        Returns:
            List of processed documents
        """
        documents = []
        
        for file_path in file_paths:
            try:
                file_path_obj = Path(file_path)
                
                if not file_path_obj.exists():
                    logger.warning(f"File does not exist: {file_path}")
                    continue
                
                file_extension = file_path_obj.suffix.lower()
                
                if file_extension not in self.supported_extensions:
                    logger.warning(f"Unsupported file type: {file_path}")
                    continue
                
                processor_func = self.supported_extensions[file_extension]
                file_documents = processor_func(file_path)
                documents.extend(file_documents)
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
        
        logger.info(f"Successfully processed {len(documents)} documents from {len(file_paths)} files")
        return documents
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Create a FAISS vector store from the processed documents.
        
        Args:
            documents: List of processed documents
            
        Returns:
            FAISS vector store
        """
        if not documents:
            logger.error("No documents provided for vector store creation")
            return None
        
        # Split documents into chunks
        logger.info("Splitting documents into chunks...")
        doc_chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(doc_chunks)} document chunks")
        
        # Create vector store
        logger.info("Creating FAISS vector store...")
        vector_store = FAISS.from_documents(doc_chunks, self.embeddings)
        
        self.vector_store = vector_store
        self.processed_documents = documents
        
        logger.info(f"Successfully created FAISS vector store with {len(doc_chunks)} chunks")
        return vector_store
    
    def save_vector_store(self, save_path: str):
        """
        Save the FAISS vector store to disk.
        
        Args:
            save_path: Path to save the vector store
        """
        if not self.vector_store:
            logger.error("No vector store to save. Create one first.")
            return
        
        try:
            self.vector_store.save_local(save_path)
            
            # Save metadata
            metadata = {
                "num_documents": len(self.processed_documents),
                "num_chunks": self.vector_store.index.ntotal,
                "embedding_model": "all-MiniLM-L6-v2",
                "processed_files": [doc.metadata.get("source", "") for doc in self.processed_documents]
            }
            
            with open(f"{save_path}/metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Vector store saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
    
    def load_vector_store(self, load_path: str) -> FAISS:
        """
        Load a FAISS vector store from disk.
        
        Args:
            load_path: Path to load the vector store from
            
        Returns:
            Loaded FAISS vector store
        """
        try:
            vector_store = FAISS.load_local(load_path, self.embeddings, allow_dangerous_deserialization=True)
            self.vector_store = vector_store
            
            # Load metadata if available
            metadata_path = f"{load_path}/metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                logger.info(f"Loaded vector store with {metadata.get('num_chunks', 'unknown')} chunks")
            
            logger.info(f"Vector store loaded from {load_path}")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return None
    
    def search_similar_documents(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for similar documents in the vector store.
        
        Args:
            query: Search query
            k: Number of similar documents to return
            
        Returns:
            List of similar documents
        """
        if not self.vector_store:
            logger.error("No vector store available. Create or load one first.")
            return []
        
        try:
            similar_docs = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(similar_docs)} similar documents for query: '{query}'")
            return similar_docs
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []


def main():
    """
    Example usage of the DocumentProcessor class.
    """
    # Initialize the processor
    processor = DocumentProcessor()
    
    # Example 1: Process a directory
    documents_dir = "Docs/"  # Replace with your documents directory
    if os.path.exists(documents_dir):
        documents = processor.process_directory(documents_dir, recursive=True)
        
        if documents:
            # Create vector store
            vector_store = processor.create_vector_store(documents)
            
            # Save vector store
            processor.save_vector_store("./vector_store")
            
            # Example search
            results = processor.search_similar_documents("Rank of the model/place?", k=3)
            
            for i, doc in enumerate(results):
                print(f"\n--- Result {i+1} ---")
                print(f"Source: {doc.metadata.get('source', 'Unknown')}")
                print(f"Type: {doc.metadata.get('type', 'Unknown')}")
                print(f"Content: {doc.page_content[:200]}...")
    
    # Example 2: Process specific files
    file_list = [
        "README.md",
        "Screenshot 2025-05-10 154749.png"
    ]
    
    # Filter for existing files
    existing_files = [f for f in file_list if os.path.exists(f)]
    
    if existing_files:
        documents = processor.process_files(existing_files)
        
        if documents:
            vector_store = processor.create_vector_store(documents)
            processor.save_vector_store("./vector_store_files")


if __name__ == "__main__":
    main()