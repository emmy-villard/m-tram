pip3 install -e .[dev]
source scripts/generate_export.env.sh

docker compose -f scripts/tests/docker-compose-airflow-tests.yml down -v --remove-orphans
docker compose -f scripts/tests/docker-compose-airflow-tests.yml up -d --force-recreate --wait