# Stage 1: Build Frontend Web Application
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python API + Static Host Server
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code & pre-generated sample documents
COPY backend/ ./backend

# Copy static frontend build output
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Environment variables for Oracle Cloud Infrastructure
ENV OCI_REGION="sa-saopaulo-1"
ENV PORT=8000

EXPOSE 8000

CMD ["python", "backend/main.py"]
