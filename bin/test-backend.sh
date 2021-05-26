#!/usr/bin/env bash

# Remove the leading backend/app/ from the command line argument so the path works inside of the container.
new_path=${1#backend/app/}

docker-compose -f docker-compose-dev.yml run -e TESTING=1 backend pytest "$new_path" -vv