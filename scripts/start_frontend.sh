#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Free port 3000 if occupied
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
sleep 1

# Start Vite Production Server
cd /tmp/nlp_clean
nohup env CI=true ./node_modules/vite/bin/vite.js preview --port 3000 --host </dev/null >"$DIR/frontend.log" 2>&1 &
echo $! > "$DIR/frontend.pid"

for i in {1..20}; do
    if curl -s http://127.0.0.1:3000/ >/dev/null 2>&1; then
        echo "QueryMind Frontend is live on http://localhost:3000 (PID $(cat "$DIR/frontend.pid"))"
        exit 0
    fi
    sleep 0.5
done

echo "QueryMind Frontend started with PID $(cat "$DIR/frontend.pid") on http://localhost:3000"
