#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Stopping PostgreSQL cluster in $DIR/data/postgres..."
"$DIR/pg_env/bin/pg_ctl" -D "$DIR/data/postgres" stop -m fast
