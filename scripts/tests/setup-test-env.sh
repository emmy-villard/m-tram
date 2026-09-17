pip3 install -e .[dev]
source scripts/tests/generate_export.env.sh

docker compose -f scripts/tests/docker-compose-test.yml --env-file .env.test down -v --remove-orphans
docker compose -f scripts/tests/docker-compose-test.yml --env-file .env.test build
docker compose -f scripts/tests/docker-compose-test.yml --env-file .env.test up -d --force-recreate --wait

alembic upgrade head