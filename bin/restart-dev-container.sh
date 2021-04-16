#!/usr/bin/env bash

bin/stop-dev-container.sh
docker-compose -f docker-compose-dev.yml up -d