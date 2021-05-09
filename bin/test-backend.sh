#!/usr/bin/env bash

docker-compose -f docker-compose-dev.yml run -e TESTING=1 backend pytest