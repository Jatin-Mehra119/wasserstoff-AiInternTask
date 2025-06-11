# RAG API Testing Suite

This folder contains comprehensive testing scripts for the RAG (Retrieval-Augmented Generation) API endpoints.

## Test Files

### 1. `test_api_endpoints.py`
A comprehensive custom testing script that provides:
- Individual endpoint testing
- Complete workflow testing
- Detailed reporting
- Command-line interface
- Automatic test file creation

### 2. `test_endpoints_pytest.py`
Pytest-based test suite for structured testing:
- Unit tests for each endpoint
- Fixtures for test data
- Parametrized tests
- Integration tests
- Coverage support

### 3. `run_tests.sh`
Bash script for easy test execution:
- Server status checking
- Dependency installation
- Test running with different options
- Coverage reporting

### 4. `requirements-test.txt`
Test-specific dependencies

## Prerequisites

1. **Start the API Server**
   ```bash
   cd /workspaces/wasserstoff-AiInternTask
   python backend/main.py
   ```

2. **Install Test Dependencies**
   ```bash
   pip install -r test/requirements-test.txt
   ```

3. **Set Environment Variables (Optional)**
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

## Running Tests

### Using the Test Runner Script

```bash
# Check if server is running
./test/run_tests.sh check

# Install test dependencies
./test/run_tests.sh install

# Run all tests
./test/run_tests.sh all

# Run custom test script
./test/run_tests.sh custom

# Run custom test script with API key
./test/run_tests.sh custom --api-key YOUR_API_KEY

# Run specific test
./test/run_tests.sh custom --test upload

# Run pytest tests
./test/run_tests.sh pytest

# Run pytest with coverage
./test/run_tests.sh coverage
```

### Using Custom Test Script Directly

```bash
# Run all tests
python test/test_api_endpoints.py

# Run all tests with API key
python test/test_api_endpoints.py --api-key YOUR_API_KEY

# Run specific test
python test/test_api_endpoints.py --test upload

# Test against different server
python test/test_api_endpoints.py --url http://localhost:8000
```

### Using Pytest Directly

```bash
# Run all pytest tests
pytest test/test_endpoints_pytest.py -v

# Run specific test
pytest test/test_endpoints_pytest.py::TestRAGAPI::test_get_stats -v

# Run with coverage
pytest test/test_endpoints_pytest.py --cov=backend --cov-report=html -v

# Run tests that require API key (with GROQ_API_KEY set)
pytest test/test_endpoints_pytest.py::TestRAGAPIWithSetup -v
```

## Test Coverage

### Endpoints Tested

1. **GET /**
   - Main page endpoint

2. **POST /set-api-key**
   - Setting GROQ API key
   - Invalid key handling

3. **GET /stats**
   - Processing statistics retrieval

4. **GET /chat-history**
   - Chat history retrieval

5. **POST /upload-files**
   - File upload and processing
   - Multiple file types
   - Error handling

6. **POST /process-directory**
   - Directory processing
   - Invalid path handling

7. **POST /chat**
   - Chat interaction
   - Response with citations and themes
   - Error handling without documents

8. **POST /save-vector-store**
   - Vector store persistence

9. **POST /load-vector-store**
   - Vector store loading

10. **DELETE /clear-chat**
    - Chat history clearing

### Test Scenarios

- **Happy Path**: Normal operation with valid inputs
- **Error Handling**: Invalid inputs, missing data, server errors
- **Edge Cases**: Empty files, large files, special characters
- **Integration**: Full workflow from upload to chat
- **Persistence**: Save/load vector store operations

## Test Results

### Custom Test Script Output
The custom test script provides detailed output including:
- Individual test results (✓/✗)
- Response data for debugging
- Summary statistics
- Error messages

### Pytest Output
Pytest provides:
- Test status for each test method
- Detailed failure information
- Coverage reports (when enabled)
- HTML reports (when configured)

## Troubleshooting

### Common Issues

1. **Server Not Running**
   ```
   ✗ Server is not running! Please start the FastAPI server first.
   ```
   **Solution**: Start the server with `python backend/main.py`

2. **API Key Not Set**
   ```
   GROQ API key is required
   ```
   **Solution**: Provide API key via `--api-key` or `GROQ_API_KEY` environment variable

3. **Dependencies Missing**
   ```
   ModuleNotFoundError: No module named 'pytest'
   ```
   **Solution**: Install test dependencies with `pip install -r test/requirements-test.txt`

4. **Port Already in Use**
   ```
   Address already in use
   ```
   **Solution**: Check if another process is using port 7860 or change the port

### Debugging Tips

1. **Check Server Logs**: Look at the FastAPI server output for error details
2. **Test Individual Endpoints**: Use `--test` flag to test specific endpoints
3. **Use Verbose Mode**: Add `-v` flag to pytest for detailed output
4. **Check Network**: Ensure localhost:7860 is accessible

## Extending Tests

### Adding New Tests

1. **Custom Script**: Add new methods to the `RAGAPITester` class
2. **Pytest**: Add new test methods to the test classes

### Example New Test

```python
def test_new_endpoint(self):
    """Test a new endpoint."""
    response = self.session.get(f"{self.BASE_URL}/new-endpoint")
    assert response.status_code == 200
    # Add more assertions
```

### Test Data

The tests automatically create temporary test files including:
- Text files with AI/ML content
- Markdown files with structured content
- Temporary directories for testing

## Performance Testing

For performance testing, you can:
1. Use tools like `locust` or `artillery`
2. Extend the test scripts with timing measurements
3. Test with larger file uploads
4. Test concurrent requests

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Run API Tests
  run: |
    python backend/main.py &
    sleep 10  # Wait for server to start
    pytest test/test_endpoints_pytest.py -v
```
