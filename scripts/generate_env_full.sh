#!/usr/bin/env bash
# Generates every variable required by generate_env.sh for a local launch,
# then runs it to write the .env file. Values already set in the shell or in
# an existing .env are kept, so re-running does not change passwords of
# existing volumes. Usage:
#   ./scripts/generate_env_full.sh
#   ATMO_API_KEY=<your key> ./scripts/generate_env_full.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

random_alnum() {
    head -c 512 /dev/urandom | tr -dc 'A-Za-z0-9' | head -c "${1:-32}"
}

random_fernet_key() {
    head -c 32 /dev/urandom | base64 | tr '+/' '-_'
}

set_default() {
    local name="$1" value="$2"
    if [[ -z "${!name:-}" ]]; then
        export "$name=$value"
    fi
}

set_default POSTGRES_PASSWORD "$(random_alnum 32)"
set_default AIRFLOW_PASSWORD "$(random_alnum 32)"
set_default FERNET_KEY "$(random_fernet_key)"
set_default AIRFLOW__API_AUTH__JWT_SECRET "$(random_alnum 64)"
set_default AIRFLOW__API_AUTH__JWT_ISSUER "mtram-local"
set_default _AIRFLOW_WWW_USER_USERNAME "admin"
set_default _AIRFLOW_WWW_USER_PASSWORD "$(random_alnum 24)"
set_default PROXY_NET_EXTERNAL "false"
set_default DASHBOARD_PROD_URL "localhost"
set_default AIRFLOW_APISERVER_PROD_URL "localhost"
# The dashboard calls the API from inside the Docker network
set_default API_PROD_URL "http://fastapi-server"

if [[ -z "${ATMO_API_KEY:-}" ]]; then
    export ATMO_API_KEY="changeme"
    echo "Warning: ATMO_API_KEY is not set; using a placeholder." >&2
    echo "The ATMO DAG will fail until you set a real key in .env" >&2
    echo "(free key: https://api.atmo-aura.fr/register)." >&2
fi

./scripts/generate_env.sh

echo ".env generated. Airflow login: ${_AIRFLOW_WWW_USER_USERNAME} / ${_AIRFLOW_WWW_USER_PASSWORD}"
