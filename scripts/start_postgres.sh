#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if "$DIR/pg_env/bin/pg_ctl" -D "$DIR/data/postgres" status >/dev/null 2>&1; then
    echo "PostgreSQL cluster is already running."
    exit 0
fi
echo "Starting PostgreSQL cluster in $DIR/data/postgres..."
"$DIR/pg_env/bin/pg_ctl" -D "$DIR/data/postgres" -l "$DIR/data/postgres/server.log" -o "-p 5432 -k /tmp" start

