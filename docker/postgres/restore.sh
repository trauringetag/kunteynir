#!/bin/bash
set -e
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-privileges /docker-entrypoint-initdb.d/initial_data.backup