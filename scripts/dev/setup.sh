./scripts/generate.env.sh
python3 -m pip install -e .
source scripts/dev/entrypoint.sh

python3 -m db_connection.init_db