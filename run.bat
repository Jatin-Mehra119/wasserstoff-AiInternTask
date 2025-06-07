@echo off
echo 🚀 Starting Agentic RAG Chat Application...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python to continue.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Set environment variables
set PYTHONPATH=%PYTHONPATH%;%cd%

REM Start the FastAPI backend
echo 🔧 Starting FastAPI backend on http://localhost:8000...
cd backend
start /b python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

REM Open browser to the frontend
echo 🌐 Opening frontend in browser...
start http://localhost:8000

echo ✅ Application is running!
echo 📖 Backend API: http://localhost:8000/api
echo 🖥️  Frontend: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo Press any key to stop the application
pause >nul

REM Stop the application
taskkill /f /im python.exe /t >nul 2>&1
echo 🛑 Application stopped.
