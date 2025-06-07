#!/bin/bash

# Agentic RAG Chat Application Launcher
echo "🚀 Starting Agentic RAG Chat Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip to continue."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the FastAPI backend
echo "🔧 Starting FastAPI backend on http://localhost:8000..."
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 3

# Open browser to the frontend
echo "🌐 Opening frontend in browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
elif command -v open &> /dev/null; then
    open http://localhost:8000
else
    echo "Please open http://localhost:8000 in your browser"
fi

echo "✅ Application is running!"
echo "📖 Backend API: http://localhost:8000/api"
echo "🖥️  Frontend: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the application"

# Wait for user to stop the application
trap 'echo "🛑 Stopping application..."; kill $BACKEND_PID; exit 0' INT
wait $BACKEND_PID
