#!/bin/bash
# Start Knowledge Platform

echo "Starting Knowledge Platform..."

# Start backend
cd "$(dirname "$0")/backend"
echo "Starting backend on port 8006..."
nohup .venv/bin/uvicorn app.api:app --host 127.0.0.1 --port 8006 > /tmp/kp_backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:8006/health > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    sleep 1
done

# Start frontend
cd "$(dirname "$0")/frontend"
echo "Starting frontend (auto-detect port)..."
nohup npm run dev > /tmp/kp_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to be ready
echo "Waiting for frontend to be ready..."
sleep 8
FRONTEND_PORT=""
for port in 3000 3001 3002 3003; do
    if curl -s "http://127.0.0.1:$port/" > /dev/null 2>&1; then
        FRONTEND_PORT=$port
        break
    fi
done

if [ -z "$FRONTEND_PORT" ]; then
    echo "Warning: Could not detect frontend port. Check /tmp/kp_frontend.log"
    FRONTEND_PORT="3001"
fi

echo ""
echo "=========================================="
echo "Knowledge Platform is running!"
echo "=========================================="
echo ""
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo "Backend API: http://localhost:8006"
echo "API Docs: http://localhost:8006/docs"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "Or run: ./stop.sh"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit" INT TERM

wait
