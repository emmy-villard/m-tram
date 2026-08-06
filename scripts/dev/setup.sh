POSTGRES_USER=app
POSTGRES_PASSWORD=$(tr -dc 'A-Za-z0-9!?%=' < /dev/urandom | head -c 32)
POSTGRES_PORT=5433
POSTGRES_DB=api_db

echo "POSTGRES_USER=$POSTGRES_USER" > .env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
echo "POSTGRES_PORT=$POSTGRES_PORT" >> .env
echo "POSTGRES_DB=$POSTGRES_DB" >> .env

python3 -m pip install -e .
source scripts/dev/entrypoint.sh