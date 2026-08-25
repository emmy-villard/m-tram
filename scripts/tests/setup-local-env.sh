pip3 install -e .
source scripts/generate_export.env.sh

docker compose -f dev_tools/docker-compose-local.yml --env-file .env down -v
docker compose -f dev_tools/docker-compose-local.yml --env-file .env up -d --force-recreate --wait