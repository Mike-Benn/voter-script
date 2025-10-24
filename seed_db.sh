#!/bin/zsh

set -e

DB_NAME="indiana_records"
USER="mike"

echo "Seeding tables..."
psql -U "$USER" -d "$DB_NAME" -f ./sql/seed.sql
echo "Table seeding complete"