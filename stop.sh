#!/bin/bash
# Stop Knowledge Platform

echo "Stopping Knowledge Platform..."

pkill -f "uvicorn app.api:app" 2>/dev/null
echo "Server stopped."
