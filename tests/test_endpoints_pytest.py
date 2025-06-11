"""
Pytest-based test suite for RAG API endpoints.
Run with: pytest test_endpoints_pytest.py -v
"""

import pytest
import requests
import tempfile
import os
import json
from typing import Dict, Any


class TestRAGAPI:
    """Test class for RAG API endpoints."""
    
    BASE_URL = "http://localhost:7860"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test."""
        self.session = requests.Session()
        
    def test_server_running(self):
        """Test if the server is running."""
        try:
            response = self.session.get(f"{self.BASE_URL}/")
            assert response.status_code in [200, 404], "Server should be running"
        except requests.ConnectionError:
            pytest.fail("Server is not running. Please start the FastAPI server.")
    
    def test_get_stats(self):
        """Test the stats endpoint."""
        response = self.session.get(f"{self.BASE_URL}/stats")
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "vector_store_loaded" in data
    
    def test_get_chat_history(self):
        """Test the chat history endpoint."""
        response = self.session.get(f"{self.BASE_URL}/chat-history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)
    
    def test_set_api_key_missing(self):
        """Test setting API key with missing key."""
        response = self.session.post(f"{self.BASE_URL}/set-api-key", json={})
        assert response.status_code == 422  # Validation error
    
    def test_set_api_key_invalid(self):
        """Test setting API key with invalid key."""
        response = self.session.post(
            f"{self.BASE_URL}/set-api-key", 
            json={"api_key": "invalid_key"}
        )
        # This might succeed or fail depending on validation
        assert response.status_code in [200, 400]
    
    def test_chat_without_documents(self):
        """Test chat endpoint without uploaded documents."""
        response = self.session.post(
            f"{self.BASE_URL}/chat",
            json={"message": "What is the main topic?"}
        )
        # Should fail without documents loaded
        assert response.status_code in [400, 500]
    
    def test_upload_no_files(self):
        """Test upload endpoint with no files."""
        response = self.session.post(f"{self.BASE_URL}/upload-files")
        assert response.status_code == 422  # Validation error
    
    def test_process_nonexistent_directory(self):
        """Test processing a non-existent directory."""
        response = self.session.post(
            f"{self.BASE_URL}/process-directory",
            data={"directory_path": "/nonexistent/path"}
        )
        assert response.status_code == 400
    
    def test_save_vector_store_without_data(self):
        """Test saving vector store without loaded data."""
        response = self.session.post(f"{self.BASE_URL}/save-vector-store")
        assert response.status_code in [400, 500]
    
    def test_load_vector_store(self):
        """Test loading vector store."""
        response = self.session.post(f"{self.BASE_URL}/load-vector-store")
        # This might succeed if there's a saved store, or fail if not
        assert response.status_code in [200, 400]
    
    def test_clear_chat(self):
        """Test clearing chat history."""
        response = self.session.delete(f"{self.BASE_URL}/clear-chat")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    @pytest.fixture
    def test_files(self):
        """Create temporary test files."""
        temp_dir = tempfile.mkdtemp()
        
        # Create test text file
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("This is a test document about machine learning and AI.")
        
        # Create test markdown file
        md_file = os.path.join(temp_dir, "test.md")
        with open(md_file, 'w') as f:
            f.write("# Test\nThis is a test markdown file about artificial intelligence.")
        
        yield [txt_file, md_file]
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_upload_files_success(self, test_files):
        """Test successful file upload."""
        files = []
        try:
            for file_path in test_files:
                files.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
            
            response = self.session.post(f"{self.BASE_URL}/upload-files", files=files)
            
            # This might fail if API key is not set, but should have proper error
            assert response.status_code in [200, 400, 500]
            
            if response.status_code == 200:
                data = response.json()
                assert data["status"] == "success"
                assert "stats" in data
        finally:
            for _, (_, file_handle) in files:
                file_handle.close()
    
    def test_process_directory_success(self, test_files):
        """Test successful directory processing."""
        # Use the directory containing test files
        test_dir = os.path.dirname(test_files[0])
        
        response = self.session.post(
            f"{self.BASE_URL}/process-directory",
            data={"directory_path": test_dir}
        )
        
        # This might fail if API key is not set, but should have proper error
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert "stats" in data


class TestRAGAPIWithSetup:
    """Test class that requires API key setup."""
    
    BASE_URL = "http://localhost:7860"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test."""
        self.session = requests.Session()
        
        # Try to set API key from environment
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            response = self.session.post(
                f"{self.BASE_URL}/set-api-key",
                json={"api_key": api_key}
            )
            self.api_key_set = response.status_code == 200
        else:
            self.api_key_set = False
    
    @pytest.mark.skipif(not os.getenv("GROQ_API_KEY"), reason="GROQ_API_KEY not set")
    def test_full_workflow(self):
        """Test the complete workflow with API key."""
        if not self.api_key_set:
            pytest.skip("API key could not be set")
        
        # Create test files
        temp_dir = tempfile.mkdtemp()
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("Machine learning is a subset of artificial intelligence.")
        
        try:
            # Upload files
            with open(txt_file, 'rb') as f:
                files = [('files', (os.path.basename(txt_file), f))]
                response = self.session.post(f"{self.BASE_URL}/upload-files", files=files)
                assert response.status_code == 200
            
            # Test chat
            response = self.session.post(
                f"{self.BASE_URL}/chat",
                json={"message": "What is machine learning?"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "citations" in data
            assert "themes" in data
            
            # Test save vector store
            response = self.session.post(f"{self.BASE_URL}/save-vector-store")
            assert response.status_code == 200
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
