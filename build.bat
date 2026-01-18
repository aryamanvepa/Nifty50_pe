@echo off
echo Building Nifty 50 P/E Tracker for production...

REM Build frontend
echo Building frontend...
cd frontend
call npm install
call npm run build
cd ..

REM Copy frontend build to backend
echo Setting up production structure...
if not exist "backend\frontend_build" mkdir backend\frontend_build
xcopy /E /I /Y frontend\build\* backend\frontend_build\

echo Build complete! Frontend build is in backend\frontend_build\
echo To run in production mode, use:
echo   cd backend ^&^& set ENVIRONMENT=production ^&^& python run_production.py
