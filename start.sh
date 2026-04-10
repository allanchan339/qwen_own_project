#!/bin/bash
# Start Knowledge Platform - Unified Server

echo "Starting Knowledge Platform..."

cd "$(dirname "$0")/backend"

# Start unified server (serves both API and frontend)
echo "Starting server on port 8080..."
nohup .venv/bin/uvicorn app.api:app --host 0.0.0.0 --port 8080 > /tmp/kp_server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

# Wait for server to be ready
echo "Waiting for server to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "Server is ready!"
        break
    fi
    sleep 1
done

echo ""
echo "=========================================="
echo "  Knowledge Platform is running!"
echo "=========================================="
echo ""
echo "  Access: http://localhost:8080"
echo "  API Docs: http://localhost:8080/docs"
echo ""
echo "  Server PID: $SERVER_PID"
echo ""
echo "Press Ctrl+C to stop"
echo "Or run: ./stop.sh"

# Wait for interrupt
trap "kill $SERVER_PID 2>/dev/null; echo 'Server stopped.'; exit" INT TERM

wait
