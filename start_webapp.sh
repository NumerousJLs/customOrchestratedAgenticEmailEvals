#!/bin/bash

# Start Email Analysis Web Application
# This script starts all required services

echo "=========================================="
echo "  Email Analysis Web Application Startup"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "backend/app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "   Run: python -m venv venv"
    exit 1
fi

echo "Starting services..."
echo ""

# Start agents
echo "🔍 Starting Analyzer Agent (port 8001)..."
source venv/bin/activate && python agents/analyzer.py &
ANALYZER_PID=$!
sleep 2

echo "⚖️  Starting Evaluator Agent (port 8002)..."
python agents/evaluator.py &
EVALUATOR_PID=$!
sleep 2

echo "📤 Starting Output Agent (port 8003)..."
python agents/output.py &
OUTPUT_PID=$!
sleep 2

echo "🌐 Starting Flask Backend (port 5000)..."
cd backend && python app.py &
BACKEND_PID=$!
cd ..
sleep 3

echo "⚛️  Starting React Frontend (port 3000)..."
cd frontend && npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "✅ All services started!"
echo "=========================================="
echo ""
echo "Services running:"
echo "  - Analyzer Agent:  http://localhost:8001 (PID: $ANALYZER_PID)"
echo "  - Evaluator Agent: http://localhost:8002 (PID: $EVALUATOR_PID)"
echo "  - Output Agent:    http://localhost:8003 (PID: $OUTPUT_PID)"
echo "  - Flask Backend:   http://localhost:5000 (PID: $BACKEND_PID)"
echo "  - React Frontend:  http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Open http://localhost:3000 in your browser"
echo ""
echo "To stop all services, press Ctrl+C"
echo "=========================================="

# Wait for all processes
wait
