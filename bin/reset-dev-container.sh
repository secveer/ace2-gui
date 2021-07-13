#!/usr/bin/env bash

# Destroy the existing development environment
docker-compose -f docker-compose-dev.yml down -v

# Initialize the new development environment
bin/initialize-dev-environment.py

# Build the new development environment
docker-compose -f docker-compose-dev.yml build

# Start the development environment
docker-compose -f docker-compose-dev.yml up -d