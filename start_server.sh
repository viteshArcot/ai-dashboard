#!/bin/bash
echo "Starting AI Dashboard Backend..."
echo "API Documentation will be available at: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/health"
echo ""
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload