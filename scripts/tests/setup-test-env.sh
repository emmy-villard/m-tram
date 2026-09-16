pip3 install -e .[dev]
source scripts/tests/generate_export.env.sh

docker compose -f scripts/tests/docker-compose-test-db.yml --env-file .env.test down -v --remove-orphans
docker compose -f scripts/tests/docker-compose-test-db.yml --env-file .env.test up -d --force-recreate --wait

docker compose -f scripts/tests/docker-compose-test-fastapi.yml --env-file .env.test down -v --remove-orphans
docker compose -f scripts/tests/docker-compose-test-fastapi.yml --env-file .env.test up -d --force-recreate --wait