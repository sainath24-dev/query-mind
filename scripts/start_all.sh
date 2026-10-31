#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "=========================================================="
echo "Starting QueryMind — Natural Language Query System"
echo "=========================================================="

# 1. Start PostgreSQL
echo "[1/3] Ensuring PostgreSQL cluster is active..."
bash "$DIR/scripts/start_postgres.sh"

# 2. Start Backend
echo "[2/3] Starting FastAPI Backend on port 8008..."
bash "$DIR/scripts/start_backend.sh"

# 3. Start Frontend
echo "[3/3] Starting Next.js Production Frontend on port 3000..."
bash "$DIR/scripts/start_frontend.sh"

echo ""
echo "QueryMind is completely online!"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8008"
echo "API Docs: http://localhost:8008/docs"
echo "=========================================================="
