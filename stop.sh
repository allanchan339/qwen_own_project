#!/bin/bash
# Stop Knowledge Platform

echo "Stopping Knowledge Platform..."

# Kill backend
pkill -f "uvicorn app.api:app" 2>/dev/null
echo "Backend stopped"

# Kill frontend
pkill -f "npm run dev" 2>/dev/null
echo "Frontend stopped"

echo "All servers stopped."
