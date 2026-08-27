export AIRFLOW_API=$(docker ps --format '{{.Names}}' | grep airflow-apiserver)
export APP_DB=$(docker ps --format '{{.Names}}' | grep "\-db")
docker exec $AIRFLOW_API airflow dags test etl_trr
docker exec $AIRFLOW_API airflow dags test etl_ligne
export request_trr="SELECT EXISTS (SELECT 1 FROM trr LIMIT 1);"
export request_ligne="SELECT EXISTS (SELECT 1 FROM ligne LIMIT 1);"
trr_exists=$(docker exec $APP_DB psql -U app -d api_db -c "$request_trr" -A -t)
ligne_exists=$(docker exec $APP_DB psql -U app -d api_db -c "$request_ligne" -A -t)

if [ "$trr_exists" != "t" ]; then
    exit 1
fi
if [ "$ligne_exists" != "t" ]; then
    exit 1
fi