#!/bin/bash

echo "========================================"
echo "  Nifty 50 P/E Tracker - Local Dev"
echo "========================================"
echo ""
echo "This will start:"
echo "  1. NSE Service (Node.js) - Port 3001"
echo "  2. Backend API (Python) - Port 8000"
echo "  3. Frontend (React) - Port 3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""
read -p "Press Enter to continue..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    kill $NSE_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start NSE Service
echo ""
echo "[1/3] Starting NSE Service..."
cd backend/nse_service
if [ ! -d "node_modules" ]; then
    echo "Installing NSE service dependencies..."
    npm install
fi
npm start &
NSE_PID=$!
cd ../..

# Wait for NSE service to start
sleep 3

# Start Backend
echo "[2/3] Starting Backend API..."
cd backend
python3 run.py 2>/dev/null || python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Frontend
echo "[3/3] Starting Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  All services starting!"
echo "========================================"
echo ""
echo "Services running:"
echo "  - NSE Service: http://localhost:3001"
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend:    http://localhost:3000"
echo ""
echo "The frontend will automatically open in your browser."
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for all processes
wait
