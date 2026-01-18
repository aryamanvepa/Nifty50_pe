#!/bin/bash

echo "Building Nifty 50 P/E Tracker for production..."

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Copy frontend build to backend
echo "Setting up production structure..."
mkdir -p backend/frontend_build
cp -r frontend/build/* backend/frontend_build/

echo "Build complete! Frontend build is in backend/frontend_build/"
echo "To run in production mode, use:"
echo "  cd backend && ENVIRONMENT=production python run_production.py"
