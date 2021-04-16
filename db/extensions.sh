# Enable the required extensions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOF
create extension pg_trgm;
EOF

# Create the "ace" database if it does not already exist
echo "SELECT 'CREATE DATABASE ace' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ace')\gexec" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"