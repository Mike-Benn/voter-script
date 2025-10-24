#!/bin/zsh

set -e

DB_NAME="indiana_records"
USER="mike"

echo "Generating schema..."
psql -U "$USER" -d "$DB_NAME" -f ./sql/schema.sql
echo "Schema generation complete"