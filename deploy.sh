#!/bin/bash

# Deployment script for Country Information AI Agent

set -e

echo "Building Docker image..."
docker build -t country-ai-agent:latest .

echo "Stopping existing container (if any)..."
docker stop country-ai-agent || true
docker rm country-ai-agent || true

echo "Starting new container..."
docker run -d \
  --name country-ai-agent \
  -p 8501:8501 \
  --env-file .env \
  --restart unless-stopped \
  country-ai-agent:latest

echo "Deployment complete! Application is running on http://localhost:8501"

