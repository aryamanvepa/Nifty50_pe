# Multi-stage build for production
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

# Python backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/build ./frontend_build

# Set environment variables
ENV ENVIRONMENT=production
ENV FRONTEND_BUILD_PATH=./frontend_build
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run_production.py"]
