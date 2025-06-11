"""
Test script for FastAPI endpoints in the RAG Chat API.
This script tests all available endpoints with various scenarios.
"""

import requests
import json
import os
import sys
import tempfile
from typing import Dict, Any
import time

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

class RAGAPITester:
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url
        self.session = requests.Session()
        self.api_key = None
        
    def test_connection(self) -> bool:
        """Test if the API server is running."""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code in [200, 404]  # 404 is OK if no frontend file
        except requests.ConnectionError:
            return False
    
    def set_api_key(self, api_key: str) -> Dict[str, Any]:
        """Test setting the GROQ API key."""
        print("Testing API key setting...")
        url = f"{self.base_url}/set-api-key"
        payload = {"api_key": api_key}
        
        response = self.session.post(url, json=payload)
        result = {
            "endpoint": "/set-api-key",
            "status_code": response.status_code,
            "response": response.json() if response.status_code != 500 else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            self.api_key = api_key
            print("✓ API key set successfully")
        else:
            print(f"✗ Failed to set API key: {result['response']}")
        
        return result
    
    def test_get_stats(self) -> Dict[str, Any]:
        """Test getting processing statistics."""
        print("Testing stats endpoint...")
        url = f"{self.base_url}/stats"
        
        response = self.session.get(url)
        result = {
            "endpoint": "/stats",
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Stats retrieved successfully")
        else:
            print(f"✗ Failed to get stats: {result['response']}")
        
        return result
    
    def test_get_chat_history(self) -> Dict[str, Any]:
        """Test getting chat history."""
        print("Testing chat history endpoint...")
        url = f"{self.base_url}/chat-history"
        
        response = self.session.get(url)
        result = {
            "endpoint": "/chat-history",
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Chat history retrieved successfully")
        else:
            print(f"✗ Failed to get chat history: {result['response']}")
        
        return result
    
    def test_upload_files(self, file_paths: list = None) -> Dict[str, Any]:
        """Test file upload endpoint."""
        print("Testing file upload endpoint...")
        url = f"{self.base_url}/upload-files"
        
        # Create test files if none provided
        if not file_paths:
            test_files = self._create_test_files()
            file_paths = test_files
        
        files = []
        try:
            for file_path in file_paths:
                files.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
            
            response = self.session.post(url, files=files)
            result = {
                "endpoint": "/upload-files",
                "status_code": response.status_code,
                "response": response.json() if response.status_code in [200, 400] else response.text,
                "success": response.status_code == 200
            }
            
            if result["success"]:
                print("✓ Files uploaded and processed successfully")
            else:
                print(f"✗ Failed to upload files: {result['response']}")
        
        finally:
            # Close file handles
            for _, (_, file_handle) in files:
                file_handle.close()
            
            # Clean up test files if we created them
            if not file_paths or file_paths == getattr(self, '_test_files', []):
                self._cleanup_test_files()
        
        return result
    
    def test_process_directory(self, directory_path: str = None) -> Dict[str, Any]:
        """Test directory processing endpoint."""
        print("Testing directory processing endpoint...")
        url = f"{self.base_url}/process-directory"
        
        # Use a test directory if none provided
        if not directory_path:
            directory_path = self._create_test_directory()
        
        payload = {"directory_path": directory_path}
        
        response = self.session.post(url, data=payload)
        result = {
            "endpoint": "/process-directory",
            "status_code": response.status_code,
            "response": response.json() if response.status_code in [200, 400] else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Directory processed successfully")
        else:
            print(f"✗ Failed to process directory: {result['response']}")
        
        return result
    
    def test_chat(self, message: str = "What is the main topic of the documents?") -> Dict[str, Any]:
        """Test chat endpoint."""
        print("Testing chat endpoint...")
        url = f"{self.base_url}/chat"
        payload = {"message": message}
        
        response = self.session.post(url, json=payload)
        result = {
            "endpoint": "/chat",
            "status_code": response.status_code,
            "response": response.json() if response.status_code in [200, 400] else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Chat response received successfully")
        else:
            print(f"✗ Chat failed: {result['response']}")
        
        return result
    
    def test_save_vector_store(self) -> Dict[str, Any]:
        """Test saving vector store."""
        print("Testing save vector store endpoint...")
        url = f"{self.base_url}/save-vector-store"
        
        response = self.session.post(url)
        result = {
            "endpoint": "/save-vector-store",
            "status_code": response.status_code,
            "response": response.json() if response.status_code in [200, 400] else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Vector store saved successfully")
        else:
            print(f"✗ Failed to save vector store: {result['response']}")
        
        return result
    
    def test_load_vector_store(self) -> Dict[str, Any]:
        """Test loading vector store."""
        print("Testing load vector store endpoint...")
        url = f"{self.base_url}/load-vector-store"
        
        response = self.session.post(url)
        result = {
            "endpoint": "/load-vector-store",
            "status_code": response.status_code,
            "response": response.json() if response.status_code in [200, 400] else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Vector store loaded successfully")
        else:
            print(f"✗ Failed to load vector store: {result['response']}")
        
        return result
    
    def test_clear_chat(self) -> Dict[str, Any]:
        """Test clearing chat history."""
        print("Testing clear chat endpoint...")
        url = f"{self.base_url}/clear-chat"
        
        response = self.session.delete(url)
        result = {
            "endpoint": "/clear-chat",
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text,
            "success": response.status_code == 200
        }
        
        if result["success"]:
            print("✓ Chat history cleared successfully")
        else:
            print(f"✗ Failed to clear chat: {result['response']}")
        
        return result
    
    def _create_test_files(self) -> list:
        """Create temporary test files for upload testing."""
        temp_dir = tempfile.mkdtemp()
        self._temp_dir = temp_dir
        test_files = []
        
        # Create a text file
        txt_file = os.path.join(temp_dir, "test_document.txt")
        with open(txt_file, 'w') as f:
            f.write("""
            This is a test document for the RAG system.
            It contains information about artificial intelligence and machine learning.
            
            Machine learning is a subset of artificial intelligence that focuses on
            algorithms that can learn and improve from experience without being
            explicitly programmed.
            
            Key concepts in machine learning include:
            - Supervised learning
            - Unsupervised learning
            - Reinforcement learning
            - Neural networks
            - Deep learning
            """)
        test_files.append(txt_file)
        
        # Create a markdown file
        md_file = os.path.join(temp_dir, "test_readme.md")
        with open(md_file, 'w') as f:
            f.write("""
            # Test README
            
            This is a test markdown document for testing the RAG system.
            
            ## About AI
            
            Artificial Intelligence (AI) is the simulation of human intelligence
            processes by machines, especially computer systems.
            
            ## Applications
            
            - Natural Language Processing
            - Computer Vision
            - Robotics
            - Expert Systems
            """)
        test_files.append(md_file)
        
        self._test_files = test_files
        return test_files
    
    def _create_test_directory(self) -> str:
        """Create a test directory with files."""
        if not hasattr(self, '_temp_dir'):
            self._create_test_files()
        return self._temp_dir
    
    def _cleanup_test_files(self):
        """Clean up temporary test files."""
        if hasattr(self, '_temp_dir') and os.path.exists(self._temp_dir):
            import shutil
            shutil.rmtree(self._temp_dir)
    
    def run_all_tests(self, api_key: str = None) -> Dict[str, Any]:
        """Run all available tests."""
        print("="*60)
        print("Starting RAG API Endpoint Tests")
        print("="*60)
        
        results = {}
        
        # Test connection
        if not self.test_connection():
            print("✗ Server is not running! Please start the FastAPI server first.")
            return {"error": "Server not available"}
        
        print("✓ Server is running")
        print("-"*40)
        
        # Set API key if provided
        if api_key:
            results["set_api_key"] = self.set_api_key(api_key)
            print("-"*40)
        
        # Test basic endpoints
        results["stats"] = self.test_get_stats()
        print("-"*40)
        
        results["chat_history"] = self.test_get_chat_history()
        print("-"*40)
        
        # Test file upload (this will also process documents)
        results["upload_files"] = self.test_upload_files()
        print("-"*40)
        
        # Test chat (only if upload was successful)
        if results["upload_files"]["success"]:
            results["chat"] = self.test_chat()
            print("-"*40)
            
            # Test vector store operations
            results["save_vector_store"] = self.test_save_vector_store()
            print("-"*40)
        
        # Test loading vector store
        results["load_vector_store"] = self.test_load_vector_store()
        print("-"*40)
        
        # Test clearing chat
        results["clear_chat"] = self.test_clear_chat()
        print("-"*40)
        
        # Test directory processing
        results["process_directory"] = self.test_process_directory()
        print("-"*40)
        
        # Summary
        print("="*60)
        print("Test Summary:")
        print("="*60)
        
        total_tests = 0
        passed_tests = 0
        
        for test_name, result in results.items():
            if isinstance(result, dict) and "success" in result:
                total_tests += 1
                if result["success"]:
                    passed_tests += 1
                    print(f"✓ {test_name}: PASSED")
                else:
                    print(f"✗ {test_name}: FAILED")
        
        print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
        
        return results


def main():
    """Main function to run the tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test RAG API endpoints")
    parser.add_argument("--url", default="http://localhost:7860", 
                       help="Base URL of the API server")
    parser.add_argument("--api-key", 
                       help="GROQ API key for testing")
    parser.add_argument("--test", choices=[
        "all", "connection", "api-key", "stats", "chat-history",
        "upload", "chat", "save-store", "load-store", "clear-chat", "directory"
    ], default="all", help="Specific test to run")
    
    args = parser.parse_args()
    
    tester = RAGAPITester(args.url)
    
    if args.test == "all":
        results = tester.run_all_tests(args.api_key)
    elif args.test == "connection":
        success = tester.test_connection()
        print(f"Connection test: {'✓ PASSED' if success else '✗ FAILED'}")
    elif args.test == "api-key":
        if not args.api_key:
            print("Please provide --api-key for this test")
            return
        result = tester.set_api_key(args.api_key)
        print(f"API key test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "stats":
        result = tester.test_get_stats()
        print(f"Stats test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "chat-history":
        result = tester.test_get_chat_history()
        print(f"Chat history test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "upload":
        result = tester.test_upload_files()
        print(f"Upload test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "chat":
        result = tester.test_chat()
        print(f"Chat test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "save-store":
        result = tester.test_save_vector_store()
        print(f"Save store test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "load-store":
        result = tester.test_load_vector_store()
        print(f"Load store test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "clear-chat":
        result = tester.test_clear_chat()
        print(f"Clear chat test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
    elif args.test == "directory":
        result = tester.test_process_directory()
        print(f"Directory test: {'✓ PASSED' if result['success'] else '✗ FAILED'}")


if __name__ == "__main__":
    main()
