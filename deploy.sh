#!/bin/bash

# Production deployment script for Meme Generator
# Run this after building the app

set -e

echo "🚀 Production Deployment Script"
echo "================================"

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "❌ Error: backend/.env file not found"
    echo "Please create it from backend/.env.example"
    exit 1
fi

# Check if frontend build exists
if [ ! -d frontend/build ]; then
    echo "❌ Error: frontend/build directory not found"
    echo "Run 'cd frontend && npm run build' first"
    exit 1
fi

echo ""
echo "✅ Pre-flight checks passed"
echo ""

# Option 1: Docker Compose (Local/VM deployment)
if command -v docker-compose &> /dev/null; then
    echo "🐳 Docker Compose detected"
    read -p "Deploy with Docker Compose? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Building and starting containers..."
        docker-compose up -d --build
        echo ""
        echo "✅ Deployment complete!"
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop: docker-compose down"
        exit 0
    fi
fi

# Option 2: Manual Azure Deployment
echo ""
echo "📦 Manual Deployment Steps:"
echo ""
echo "Backend (Azure App Service):"
echo "  1. cd backend"
echo "  2. az webapp up --name <your-backend-app> --resource-group <your-rg> --runtime PYTHON:3.12"
echo ""
echo "Frontend (Azure Static Web Apps):"
echo "  1. cd frontend/build"
echo "  2. az staticwebapp deploy --name <your-frontend-app> --resource-group <your-rg>"
echo ""
echo "Or use Docker:"
echo "  docker build -t meme-backend:latest -f backend/Dockerfile backend/"
echo "  docker tag meme-backend:latest <your-registry>.azurecr.io/meme-backend:latest"
echo "  docker push <your-registry>.azurecr.io/meme-backend:latest"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
