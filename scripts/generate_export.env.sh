write_variables() {
    # Db variables
    POSTGRES_USER=app
    POSTGRES_PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
    POSTGRES_DB=api_db
    DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@airflow_metadata_db/$POSTGRES_DB"
    echo "POSTGRES_USER=$POSTGRES_USER" > .env
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
    echo "POSTGRES_DB=$POSTGRES_DB" >> .env
    echo "DATABASE__SQL_ALCHEMY_CONN=$DATABASE__SQL_ALCHEMY_CONN" >> .env

    # Airflow variables
    AIRFLOW_USER=airflow
    AIRFLOW_PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
    AIRFLOW_DB=airflow
    AIRFLOW_APISERVER_EXTERNAL_PORT=8080
    APISERVER_URL="http://airflow-apiserver:8080"
    AIRFLOW_PROJ_DIR=./airflow
    ENV_FILE_PATH=".env"
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$AIRFLOW_USER:$AIRFLOW_PASSWORD@airflow_metadata_db/$AIRFLOW_DB"
    AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql+psycopg2://$AIRFLOW_USER:$AIRFLOW_PASSWORD@airflow_metadata_db/$AIRFLOW_DB
    AIRFLOW_IMAGE_NAME="mtram-airflow:latest"
    FERNET_KEY=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 264)
    AIRFLOW__API_AUTH__JWT_SECRET=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 264)
    AIRFLOW__API_AUTH__JWT_ISSUER=airflow_$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)
    _AIRFLOW_WWW_USER_USERNAME=airflow_$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)
    _AIRFLOW_WWW_USER_PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
    echo "AIRFLOW_UID=$(id -u)" >> .env
    echo "AIRFLOW_USER=$AIRFLOW_USER" >> .env
    echo "AIRFLOW_PASSWORD=$AIRFLOW_PASSWORD" >> .env
    echo "AIRFLOW_DB=$AIRFLOW_DB" >> .env
    echo "AIRFLOW_APISERVER_EXTERNAL_PORT=$AIRFLOW_APISERVER_EXTERNAL_PORT" >> .env
    echo "APISERVER_URL=$APISERVER_URL" >> .env
    echo "AIRFLOW_PROJ_DIR=$AIRFLOW_PROJ_DIR" >> .env
    echo "ENV_FILE_PATH=$ENV_FILE_PATH" >> .env
    echo "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=$AIRFLOW__DATABASE__SQL_ALCHEMY_CONN" >> .env
    echo "AIRFLOW__CELERY__RESULT_BACKEND=$AIRFLOW__CELERY__RESULT_BACKEND" >> .env
    echo "AIRFLOW_IMAGE_NAME=$AIRFLOW_IMAGE_NAME" >> .env
    echo "FERNET_KEY=$FERNET_KEY" >> .env
    echo "AIRFLOW__API_AUTH__JWT_SECRET=$AIRFLOW__API_AUTH__JWT_SECRET" >> .env
    echo "AIRFLOW__API_AUTH__JWT_ISSUER=$AIRFLOW__API_AUTH__JWT_ISSUER" >> .env
    echo "_AIRFLOW_WWW_USER_USERNAME=$_AIRFLOW_WWW_USER_USERNAME" >> .env
    echo "_AIRFLOW_WWW_USER_PASSWORD=$_AIRFLOW_WWW_USER_PASSWORD" >> .env
}

export_variables() {
    set -a
    source .env
    set +a
}

if [ -e .env ]
then
	printf '%s\n' 'Error: .env already exists; not overwritten' >&2
else
    write_variables
fi

export_variables