#!/bin/bash

# Test script for RAG API endpoints
# This script helps run different types of tests

echo "RAG API Test Runner"
echo "==================="

# Function to check if server is running
check_server() {
    echo "Checking if server is running..."
    if curl -s http://localhost:7860/ > /dev/null 2>&1; then
        echo "✓ Server is running"
        return 0
    else
        echo "✗ Server is not running"
        echo "Please start the server first with: python backend/main.py"
        return 1
    fi
}

# Function to install test dependencies
install_deps() {
    echo "Installing test dependencies..."
    pip install -r test/requirements-test.txt
}

# Function to run custom test script
run_custom_tests() {
    echo "Running custom test script..."
    cd "$(dirname "$0")/.."
    python test/test_api_endpoints.py "$@"
}

# Function to run pytest tests
run_pytest() {
    echo "Running pytest tests..."
    cd "$(dirname "$0")/.."
    pytest test/test_endpoints_pytest.py -v "$@"
}

# Function to run pytest with coverage
run_pytest_coverage() {
    echo "Running pytest with coverage..."
    cd "$(dirname "$0")/.."
    pytest test/test_endpoints_pytest.py --cov=backend --cov-report=html --cov-report=term -v
}

# Function to run all tests
run_all_tests() {
    echo "Running all tests..."
    check_server || exit 1
    
    echo ""
    echo "1. Running custom test script..."
    echo "--------------------------------"
    run_custom_tests --test all
    
    echo ""
    echo "2. Running pytest tests..."
    echo "-------------------------"
    run_pytest
}

# Parse command line arguments
case "$1" in
    "check")
        check_server
        ;;
    "install")
        install_deps
        ;;
    "custom")
        shift
        check_server || exit 1
        run_custom_tests "$@"
        ;;
    "pytest")
        shift
        check_server || exit 1
        run_pytest "$@"
        ;;
    "coverage")
        check_server || exit 1
        run_pytest_coverage
        ;;
    "all")
        run_all_tests
        ;;
    *)
        echo "Usage: $0 {check|install|custom|pytest|coverage|all} [additional args]"
        echo ""
        echo "Commands:"
        echo "  check     - Check if the API server is running"
        echo "  install   - Install test dependencies"
        echo "  custom    - Run the custom test script"
        echo "  pytest    - Run pytest tests"
        echo "  coverage  - Run pytest with coverage report"
        echo "  all       - Run all tests"
        echo ""
        echo "Examples:"
        echo "  $0 check"
        echo "  $0 install"
        echo "  $0 custom --api-key YOUR_API_KEY"
        echo "  $0 pytest -k test_upload"
        echo "  $0 coverage"
        echo "  $0 all"
        exit 1
        ;;
esac
