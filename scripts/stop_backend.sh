#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

if [ -f "$DIR/backend.pid" ]; then
    kill -9 $(cat "$DIR/backend.pid") 2>/dev/null || true
    rm -f "$DIR/backend.pid"
fi
lsof -ti :8008 | xargs kill -9 2>/dev/null || true
echo "Backend stopped."
