#!/bin/bash

echo "🚀 Starting AI Dashboard Full Stack Application"
echo ""

# Start backend in background
echo "📡 Starting Backend (FastAPI)..."
cd /workspaces/ai-dashboard
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend (React)..."
cd /workspaces/ai-dashboard/frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Application started successfully!"
echo ""
echo "🔗 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait