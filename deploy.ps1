# PowerShell deployment script for Country Information AI Agent

Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t country-ai-agent:latest .

Write-Host "Stopping existing container (if any)..." -ForegroundColor Yellow
docker stop country-ai-agent -ErrorAction SilentlyContinue
docker rm country-ai-agent -ErrorAction SilentlyContinue

Write-Host "Starting new container..." -ForegroundColor Green
docker run -d `
  --name country-ai-agent `
  -p 8501:8501 `
  --env-file .env `
  --restart unless-stopped `
  country-ai-agent:latest

Write-Host "Deployment complete! Application is running on http://localhost:8501" -ForegroundColor Green

