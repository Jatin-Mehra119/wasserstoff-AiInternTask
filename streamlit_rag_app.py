import streamlit as st
import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add the rag_elements directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'rag_elements'))

from rag_elements.enhanced_vectordb import EnhancedDocumentProcessor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic RAG Chat App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    .citation-box {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .theme-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .metrics-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

class AgenticRAGChatApp:
    """Main Streamlit chat application class."""
    
    def __init__(self):
        self.vector_store_path = "vector_store"
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "vector_store_loaded" not in st.session_state:
            st.session_state.vector_store_loaded = False
        if "documents_processed" not in st.session_state:
            st.session_state.documents_processed = 0
        if "processing_stats" not in st.session_state:
            st.session_state.processing_stats = {}
        if "processor" not in st.session_state:
            st.session_state.processor = None
    
    def initialize_processor(self):
        """Initialize the document processor."""
        if not st.session_state.processor:
            groq_api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
            if groq_api_key:
                st.session_state.processor = EnhancedDocumentProcessor(groq_api_key)
                return True
            else:
                st.error("GROQ API key is required. Please set it in the sidebar.")
                return False
        return True
    
    @property
    def processor(self):
        """Get the processor from session state."""
        return st.session_state.processor
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        st.sidebar.title("🔧 Configuration")
        
        # API Key input
        groq_api_key = st.sidebar.text_input(
            "GROQ API Key",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Enter your GROQ API key for OCR and chat capabilities"
        )
        
        # Reset processor if API key changed
        if st.session_state.get("groq_api_key") != groq_api_key:
            st.session_state.processor = None
        
        st.session_state.groq_api_key = groq_api_key
        
        st.sidebar.divider()
        
        # Document upload and processing
        st.sidebar.subheader("📁 Documents")
        
        # File uploader
        uploaded_files = st.sidebar.file_uploader(
            "Upload Documents",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'md', 'py', 'js', 'html', 'csv', 'json', 'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
            help="Upload up to 75+ documents in various formats"
        )
        
        # Process uploaded files
        if uploaded_files:
            if st.sidebar.button("🚀 Process Documents", type="primary"):
                self.process_uploaded_files(uploaded_files)
        
        # Directory processing option
        st.sidebar.subheader("📂 Directory Processing")
        directory_path = st.sidebar.text_input("Directory Path", help="Enter path to directory containing documents")
        
        if directory_path and st.sidebar.button("📁 Process Directory"):
            self.process_directory(directory_path)
        
        st.sidebar.divider()
        
        # Vector store management
        st.sidebar.subheader("🗄️ Vector Store")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("💾 Save"):
                self.save_vector_store()
        with col2:
            if st.button("📂 Load"):
                self.load_vector_store()
        
        # Display processing stats
        if st.session_state.processing_stats:
            st.sidebar.subheader("📊 Stats")
            stats = st.session_state.processing_stats
            st.sidebar.metric("Files", stats.get("total_files", 0))
            st.sidebar.metric("Documents", stats.get("total_documents", 0))
            st.sidebar.metric("Chunks", stats.get("total_chunks", 0))
            st.sidebar.metric("File Types", len(stats.get("file_types", [])))
    
    def process_uploaded_files(self, uploaded_files):
        """Process uploaded files."""
        if not self.initialize_processor():
            return
        
        try:
            with st.spinner("Processing uploaded documents..."):
                # Create temporary directory
                temp_dir = tempfile.mkdtemp()
                temp_files = []
                
                # Save uploaded files to temp directory
                for uploaded_file in uploaded_files:
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())
                    temp_files.append(temp_path)
                
                # Process files
                documents = self.processor.process_files(temp_files)
                
                if documents:
                    # Create vector store
                    vector_store = self.processor.create_enhanced_vector_store(documents)
                    
                    if vector_store:
                        st.session_state.vector_store_loaded = True
                        st.session_state.documents_processed = len(documents)
                        
                        # Track original files and their types
                        original_files = {}
                        file_type_counts = {}
                        total_chunks = vector_store.index.ntotal
                        
                        # Count unique source files and their types
                        for doc in documents:
                            source_file = doc.metadata.get("source", "unknown")
                            doc_type = doc.metadata.get("type", "unknown")
                            
                            if source_file not in original_files:
                                original_files[source_file] = doc_type
                                file_type_counts[doc_type] = file_type_counts.get(doc_type, 0) + 1
                        
                        st.session_state.processing_stats = {
                            "total_files": len(original_files),
                            "total_documents": len(documents),
                            "total_chunks": total_chunks,
                            "file_types": list(file_type_counts.keys()),
                            "type_counts": file_type_counts,
                            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.success(f"✅ Successfully processed {len(original_files)} files ({len(documents)} documents) with {total_chunks} chunks!")
                        
                        # Display processing summary
                        self.display_processing_summary(documents, file_type_counts, len(original_files))
                    else:
                        st.error("❌ Failed to create vector store.")
                else:
                    st.error("❌ No documents were processed successfully.")
                
                # Clean up temp files
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")
    
    def process_directory(self, directory_path: str):
        """Process documents from a directory."""
        if not self.initialize_processor():
            return
        
        if not os.path.exists(directory_path):
            st.error(f"❌ Directory does not exist: {directory_path}")
            return
        
        try:
            with st.spinner("Processing directory..."):
                documents = self.processor.process_directory(directory_path, recursive=True)
                
                if documents:
                    vector_store = self.processor.create_enhanced_vector_store(documents)
                    
                    if vector_store:
                        st.session_state.vector_store_loaded = True
                        st.session_state.documents_processed = len(documents)
                        
                        # Track original files and their types
                        original_files = {}
                        file_type_counts = {}
                        total_chunks = vector_store.index.ntotal
                        
                        # Count unique source files and their types
                        for doc in documents:
                            source_file = doc.metadata.get("source", "unknown")
                            doc_type = doc.metadata.get("type", "unknown")
                            
                            if source_file not in original_files:
                                original_files[source_file] = doc_type
                                file_type_counts[doc_type] = file_type_counts.get(doc_type, 0) + 1
                        
                        st.session_state.processing_stats = {
                            "total_files": len(original_files),
                            "total_documents": len(documents),
                            "total_chunks": total_chunks,
                            "file_types": list(file_type_counts.keys()),
                            "type_counts": file_type_counts,
                            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        st.success(f"✅ Successfully processed {len(original_files)} files ({len(documents)} documents) from directory!")
                        self.display_processing_summary(documents, file_type_counts, len(original_files))
                    else:
                        st.error("❌ Failed to create vector store.")
                else:
                    st.error("❌ No documents found or processed in the directory.")
        
        except Exception as e:
            st.error(f"❌ Error processing directory: {str(e)}")
    
    def display_processing_summary(self, documents: List, file_types: Dict[str, int], total_files: int):
        """Display a summary of processed documents."""
        st.subheader("📋 Processing Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Files Uploaded", total_files)
        
        with col2:
            st.metric("Total Pages", len(documents))
        
        with col3:
            total_words = sum(doc.metadata.get("word_count", 0) for doc in documents)
            st.metric("Total Words", f"{total_words:,}")
        
        with col4:
            st.metric("File Types", len(file_types))
        
        # File type distribution chart
        if file_types:
            fig = px.pie(
                values=list(file_types.values()),
                names=list(file_types.keys()),
                title="File Types Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def save_vector_store(self):
        """Save the current vector store."""
        if not st.session_state.processor or not st.session_state.processor.vector_store:
            st.error("❌ No vector store to save. Process documents first.")
            return
        
        try:
            st.session_state.processor.save_vector_store(self.vector_store_path)
            st.success("✅ Vector store saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving vector store: {str(e)}")
    
    def load_vector_store(self):
        """Load a previously saved vector store."""
        if not self.initialize_processor():
            return
        
        try:
            vector_store = self.processor.load_vector_store(self.vector_store_path)
            if vector_store:
                st.session_state.vector_store_loaded = True
                st.success("✅ Vector store loaded successfully!")
                
                # Load metadata if available
                metadata_path = f"{self.vector_store_path}/enhanced_metadata.json"
                if os.path.exists(metadata_path):
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    
                    # Calculate unique files from processed files
                    processed_files = metadata.get("processed_files", [])
                    unique_files = len(set(f.get("file_path", f.get("source", "")) for f in processed_files))
                    
                    st.session_state.processing_stats = {
                        "total_files": unique_files,
                        "total_documents": metadata.get("num_documents", 0),
                        "total_chunks": metadata.get("num_chunks", 0),
                        "file_types": list(set(f["type"] for f in processed_files if "type" in f)),
                        "processed_at": metadata.get("created_at", "Unknown")
                    }
            else:
                st.error("❌ Failed to load vector store. Check if it exists.")
        except Exception as e:
            st.error(f"❌ Error loading vector store: {str(e)}")
    
    def render_chat_interface(self):
        """Render the main chat interface."""
        st.markdown('<h1 class="main-header">📚 Agentic RAG Chat Application</h1>', unsafe_allow_html=True)
        
        if not st.session_state.vector_store_loaded:
            st.info("👈 Please upload and process documents using the sidebar to start chatting!")
            return
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display citations if available
                if "citations" in message and message["citations"]:
                    st.subheader("📖 Citations")
                    for i, citation in enumerate(message["citations"], 1):
                        with st.expander(f"Citation {i}: {citation['citation']}", expanded=False):
                            st.write(f"**Content:** {citation['content'][:300]}...")
                            st.write(f"**Score:** {citation['score']:.3f}")
                            st.write(f"**Type:** {citation['type']}")
                            if citation.get('page'):
                                st.write(f"**Page:** {citation['page']}")
                
                # Display themes if available
                if "themes" in message and message["themes"]:
                    st.subheader("🎯 Common Themes")
                    themes_data = message["themes"]
                    
                    if themes_data.get("themes"):
                        for theme in themes_data["themes"]:
                            st.markdown(f"""
                            <div class="theme-box">
                                <strong>{theme['name']}</strong><br>
                                {theme['description']}<br>
                                <em>Frequency: {theme['frequency']}</em>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if themes_data.get("summary"):
                        st.write("**Summary:**", themes_data["summary"])
                    
                    if themes_data.get("insights"):
                        st.write("**Key Insights:**")
                        for insight in themes_data["insights"]:
                            st.write(f"• {insight}")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            self.process_chat_message(prompt)
    
    def process_chat_message(self, prompt: str):
        """Process a chat message and generate response."""
        if not self.initialize_processor():
            return
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents and analyzing themes..."):
                try:
                    # Search for relevant documents
                    search_results = self.processor.search_with_citations(prompt, k=5)
                    
                    if not search_results:
                        response = "I couldn't find any relevant information in the documents for your query."
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        return
                    
                    # Analyze themes
                    theme_analysis = self.processor.analyze_themes(prompt, search_results)
                    
                    # Generate response based on search results
                    response = self.generate_response(prompt, search_results, theme_analysis)
                    
                    # Display response
                    st.markdown(response)
                    
                    # Display citations
                    st.subheader("📖 Citations")
                    for i, citation in enumerate(search_results, 1):
                        with st.expander(f"Citation {i}: {citation['citation']}", expanded=False):
                            st.write(f"**Content:** {citation['content'][:300]}...")
                            st.write(f"**Relevance Score:** {citation['score']:.3f}")
                            st.write(f"**Type:** {citation['type']}")
                            if citation.get('page'):
                                st.write(f"**Page:** {citation['page']}")
                    
                    # Display theme analysis
                    if theme_analysis and theme_analysis.get("themes"):
                        st.subheader("🎯 Common Themes")
                        
                        for theme in theme_analysis["themes"]:
                            st.markdown(f"""
                            <div class="theme-box">
                                <strong>{theme['name']}</strong><br>
                                {theme['description']}<br>
                                <em>Frequency: {theme['frequency']}</em>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if theme_analysis.get("summary"):
                            st.write("**Summary:**", theme_analysis["summary"])
                        
                        if theme_analysis.get("insights"):
                            st.write("**Key Insights:**")
                            for insight in theme_analysis["insights"]:
                                st.write(f"• {insight}")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "citations": search_results,
                        "themes": theme_analysis
                    })
                
                except Exception as e:
                    error_msg = f"❌ Error processing your question: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    def generate_response(self, query: str, search_results: List[Dict], theme_analysis: Dict) -> str:
        """Generate a comprehensive response based on search results and theme analysis."""
        if not self.processor.chat_llm:
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
            
            llm_response = self.processor.chat_llm.invoke(response_prompt)
            return llm_response.content
            
        except Exception as e:
            # Fallback to simple response
            return f"Based on your query '{query}', I found relevant information in {len(search_results)} document sections. Please see the citations below for detailed information."
    
    def run(self):
        """Run the Streamlit application."""
        # Render sidebar
        self.render_sidebar()
        
        # Render main chat interface
        self.render_chat_interface()

# Main application
def main():
    app = AgenticRAGChatApp()
    app.run()

if __name__ == "__main__":
    main()
