# Usage: source scripts/tests/run_streamlit.sh
# Resets the test env, seeds it with fake data and starts the dashboard on http://localhost:8501
source scripts/tests/setup-test-env.sh
python tests/streamlit_dashboard/seed_test_db.py

COMPOSE="docker compose -f scripts/tests/docker-compose-test.yml --env-file .env.test"
# Only the app services are rebuilt: restarting test_db would erase the seeded data
$COMPOSE down fastapi-server streamlit-dashboard
$COMPOSE build fastapi-server streamlit-dashboard
$COMPOSE up -d --wait fastapi-server streamlit-dashboard
echo "Dashboard: http://localhost:8501"
