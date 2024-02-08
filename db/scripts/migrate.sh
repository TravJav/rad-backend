#!/bin/bash

set -o errexit -o pipefail -o nounset

# Create $DB_NAME if not exists
echo "SELECT 'CREATE DATABASE ${DB_NAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DB_NAME}')\gexec" | PGPASSWORD="${DB_PASSWORD}" psql -h "${DB_DSN}" -p "${DB_PORT}" -U "${DB_USERNAME}" -d "${DB_NAME_ROOT}"

# uncomment to Create a testing database locally
# echo "SELECT 'CREATE DATABASE data-migration WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{$POSTGRES_DB}')\gexec" | PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${DB_DSN}" -p "${DB_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"

# Now run the migrations as usual against $DB_NAME
exec ./scripts/run-migrations.sh update