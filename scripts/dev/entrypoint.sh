#!/usr/bin/env bash

source scripts/setup_env_var.sh

docker compose -f dev_tools/docker-compose-local-db.yml --env-file .env down -v
docker compose -f dev_tools/docker-compose-local-db.yml --env-file .env up -d --force-recreate --wait
