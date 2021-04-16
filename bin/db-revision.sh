#!/usr/bin/env bash

# Start the entire application and then pause until the database is accessible.
# NOTE: If you changed the mapped port for the "db" service in the docker-compose-dev.yml
# file, you will need to update it below in the "while" loop as well.
docker-compose -f docker-compose-dev.yml up -d
while !</dev/tcp/localhost/6666; do sleep 1; done;

# Create the database revision
docker exec ace2-gui-backend alembic revision --autogenerate -m "$1"