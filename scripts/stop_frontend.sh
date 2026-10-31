#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "$DIR/frontend.pid" ]; then
    PID=$(cat "$DIR/frontend.pid")
    echo "Stopping QueryMind Frontend (PID $PID)..."
    kill "$PID" 2>/dev/null || true
    rm -f "$DIR/frontend.pid"
fi

lsof -ti :3000 | xargs kill -9 2>/dev/null || true
echo "Frontend stopped."
