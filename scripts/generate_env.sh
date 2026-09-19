required_variables=(
    POSTGRES_PASSWORD
    AIRFLOW_PASSWORD
    FERNET_KEY
    AIRFLOW__API_AUTH__JWT_SECRET
    AIRFLOW__API_AUTH__JWT_ISSUER
    _AIRFLOW_WWW_USER_USERNAME
    _AIRFLOW_WWW_USER_PASSWORD
    ATMO_API_KEY
    PROXY_NET_EXTERNAL
)

find_missing_variables() {
    missing_variables=()

    for variable_name in "${required_variables[@]}"; do
        if [[ -z "${!variable_name:-}" ]]; then
            missing_variables+=("$variable_name")
        fi
    done
}

echo_variable() {
    echo "$1=${!1}"
}

write_variables() {
    # Db variables
    POSTGRES_USER=app
    POSTGRES_DB=api_db
    DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@db/$POSTGRES_DB"
    echo_variable POSTGRES_USER > .env
    echo_variable POSTGRES_DB >> .env
    echo_variable DATABASE__SQL_ALCHEMY_CONN >> .env

    # Airflow variables
    AIRFLOW_USER=airflow
    AIRFLOW_DB=airflow
    AIRFLOW_WEBUI_DEV_PORT=8080
    FASTAPI_DEV_PORT=8081
    APISERVER_URL="http://airflow-apiserver:8080"
    AIRFLOW_PROJ_DIR=./airflow
    ENV_FILE_PATH=".env"
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$AIRFLOW_USER:$AIRFLOW_PASSWORD@airflow_metadata_db/$AIRFLOW_DB"
    AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql+psycopg2://$AIRFLOW_USER:$AIRFLOW_PASSWORD@airflow_metadata_db/$AIRFLOW_DB
    AIRFLOW_IMAGE_NAME="mtram-airflow:latest"
    AIRFLOW_UID=$(id -u)
    echo_variable AIRFLOW_UID >> .env
    echo_variable AIRFLOW_USER >> .env
    echo_variable AIRFLOW_DB >> .env
    echo_variable AIRFLOW_WEBUI_DEV_PORT >> .env
    echo_variable FASTAPI_DEV_PORT >> .env
    echo_variable APISERVER_URL >> .env
    echo_variable AIRFLOW_PROJ_DIR >> .env
    echo_variable ENV_FILE_PATH >> .env
    echo_variable AIRFLOW__DATABASE__SQL_ALCHEMY_CONN >> .env
    echo_variable AIRFLOW__CELERY__RESULT_BACKEND >> .env
    echo_variable AIRFLOW_IMAGE_NAME >> .env

    #FastAPI
    FASTAPI_IMAGE="mtram-fastapi:latest"
    echo_variable FASTAPI_IMAGE >> .env

    # Secrets
    echo_variable POSTGRES_PASSWORD >> .env
    echo_variable AIRFLOW_PASSWORD >> .env
    echo_variable FERNET_KEY >> .env
    echo_variable AIRFLOW__API_AUTH__JWT_SECRET >> .env
    echo_variable AIRFLOW__API_AUTH__JWT_ISSUER >> .env
    echo_variable _AIRFLOW_WWW_USER_USERNAME >> .env
    echo_variable _AIRFLOW_WWW_USER_PASSWORD >> .env
    echo_variable ATMO_API_KEY >> .env

    # Dev/Prod distinct variables
    echo_variable PROXY_NET_EXTERNAL >> .env
}

find_missing_variables
if (( ${#missing_variables[@]} > 0 )) && [[ -f .env ]]; then
    set -a
    source .env
    set +a
    find_missing_variables
fi
if (( ${#missing_variables[@]} > 0 )); then
    printf 'Error: required variables are missing:\n' >&2
    printf '  %s\n' "${missing_variables[@]}" >&2
    exit 1
fi

write_variables