@echo off
echo ========================================
echo   Nifty 50 P/E Tracker - Local Dev
echo ========================================
echo.
echo This will start:
echo   1. NSE Service (Node.js) - Port 3001
echo   2. Backend API (Python) - Port 8000
echo   3. Frontend (React) - Port 3000
echo.
echo Press Ctrl+C to stop all services
echo.
pause

REM Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Start NSE Service in a new window
echo.
echo [1/3] Starting NSE Service...
start "NSE Service" cmd /k "cd backend\nse_service && if exist node_modules (npm start) else (echo Installing NSE service dependencies... && npm install && npm start)"

REM Wait a bit for NSE service to start
timeout /t 3 /nobreak >nul

REM Start Backend in a new window
echo [2/3] Starting Backend API...
start "Backend API" cmd /k "cd backend && python run.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend in a new window
echo [3/3] Starting Frontend...
start "Frontend" cmd /k "cd frontend && if exist node_modules (npm start) else (echo Installing frontend dependencies... && npm install && npm start)"

echo.
echo ========================================
echo   All services starting!
echo ========================================
echo.
echo Services will open in separate windows:
echo   - NSE Service: http://localhost:3001
echo   - Backend API: http://localhost:8000
echo   - Frontend:    http://localhost:3000
echo.
echo The frontend will automatically open in your browser.
echo.
echo To stop all services, close the command windows or press Ctrl+C in each.
echo.
pause
