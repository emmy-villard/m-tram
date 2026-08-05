#!/usr/bin/env bash

docker compose -f dev_tools/docker-compose-local-db.yml --env-file .env down -v
docker compose -f dev_tools/docker-compose-local-db.yml --env-file .env up -d --force-recreate

set -a
source .env
set +a