@echo off
REM GeoShield AI - Quick Start Script (Windows)
REM This script starts both frontend and backend servers

echo.
echo 🛡️  GeoShield AI - Cyber Threat Intelligence Platform
echo ==================================================

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i

echo ✅ Node.js version: %NODE_VERSION%
echo ✅ Python version: %PYTHON_VERSION%

REM Start Backend
echo.
echo 🚀 Starting Backend Server...
echo ==================================================

cd server

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
python -c "import flask" >nul 2>nul
if %errorlevel% neq 0 (
    echo 📥 Installing Python dependencies...
    pip install -r requirements.txt
)

REM Start Flask server in new window
start "GeoShield Backend" python app.py
echo ✅ Backend server started in new window
timeout /t 3 /nobreak

REM Start Frontend
echo.
echo 🚀 Starting Frontend Server...
echo ==================================================

cd ..\client

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📥 Installing Node dependencies...
    call npm install
)

REM Start Vite dev server in new window
start "GeoShield Frontend" npm run dev
echo ✅ Frontend server started in new window
timeout /t 3 /nobreak

echo.
echo ==================================================
echo 🎉 GeoShield AI is running!
echo ==================================================
echo.
echo 📍 Frontend: http://localhost:5173
echo 📍 Backend:  http://127.0.0.1:5000
echo.
echo 🔐 Demo Credentials:
echo    Email: officer@geoshield.ai
echo    Password: password
echo.
echo 📖 Check the opened windows for server logs
echo ❌ To stop, close the server windows
echo.
pause
