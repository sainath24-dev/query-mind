#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "Stopping QueryMind Services..."
bash "$DIR/scripts/stop_frontend.sh" || true
bash "$DIR/scripts/stop_backend.sh" || true
bash "$DIR/scripts/stop_postgres.sh" || true
echo "All QueryMind services stopped cleanly."
