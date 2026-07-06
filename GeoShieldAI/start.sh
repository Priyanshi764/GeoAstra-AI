#!/bin/bash

# GeoShield AI - Quick Start Script
# This script starts both frontend and backend servers

echo "🛡️  GeoShield AI - Cyber Threat Intelligence Platform"
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python version: $(python3 --version)"

# Start Backend
echo ""
echo "🚀 Starting Backend Server..."
echo "=================================================="
cd server

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start Flask server in background
python3 app.py &
BACKEND_PID=$!
echo "Backend server PID: $BACKEND_PID"
sleep 3

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend server failed to start"
    exit 1
fi

echo "✅ Backend running on http://127.0.0.1:5000"

# Start Frontend
echo ""
echo "🚀 Starting Frontend Server..."
echo "=================================================="
cd ../client

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Node dependencies..."
    npm install
fi

# Start Vite dev server
npm run dev &
FRONTEND_PID=$!
echo "Frontend server PID: $FRONTEND_PID"
sleep 3

echo "✅ Frontend running on http://localhost:5173"

echo ""
echo "=================================================="
echo "🎉 GeoShield AI is running!"
echo "=================================================="
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend:  http://127.0.0.1:5000"
echo ""
echo "🔐 Demo Credentials:"
echo "   Email: officer@geoshield.ai"
echo "   Password: password"
echo ""
echo "❌ To stop, press Ctrl+C"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
