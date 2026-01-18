@echo off
echo Starting Nifty 50 P/E Tracker Backend...
echo.
echo Make sure you have:
echo 1. Python dependencies installed (pip install -r requirements.txt)
echo 2. NSE service running (optional, will use fallback if not available)
echo.
echo Backend will run on http://localhost:8000
echo.
cd backend
python run.py
pause
