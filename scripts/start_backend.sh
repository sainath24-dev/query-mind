#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

# Free port 8008 if occupied
lsof -ti :8008 | xargs kill -9 2>/dev/null || true
sleep 1

PYTHON_EXEC="/opt/anaconda3/bin/python3"
if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC="$DIR/.venv/bin/python"
fi

PYTHONPATH="$DIR" nohup "$PYTHON_EXEC" "$DIR/scripts/run_server.py" </dev/null >"$DIR/backend.log" 2>&1 &
echo $! > "$DIR/backend.pid"

for i in {1..20}; do
    if curl -s http://127.0.0.1:8008/ >/dev/null 2>&1; then
        echo "QueryMind Backend is live on http://127.0.0.1:8008 (PID $(cat "$DIR/backend.pid"))"
        exit 0
    fi
    sleep 0.5
done

echo "QueryMind Backend started with PID $(cat "$DIR/backend.pid") on port 8008"
