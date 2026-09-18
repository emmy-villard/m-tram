set -a
source .env
set +a

APP_DB=$(docker ps --format '{{.Names}}' | grep "\-db")

docker compose exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom \
  > "db_backups/db-$(date +%F-%H%M%S).dump"