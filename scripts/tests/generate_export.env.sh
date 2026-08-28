write_variables() {
    # Test db variables
    POSTGRES_TEST_USER=test
    POSTGRES_TEST_PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 32)
    POSTGRES_TEST_PORT=54320
    POSTGRES_TEST_HOST=localhost
    POSTGRES_TEST_DB=test_db
    TEST_DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$POSTGRES_TEST_USER:$POSTGRES_TEST_PASSWORD@$POSTGRES_TEST_HOST:$POSTGRES_TEST_PORT/$POSTGRES_TEST_DB"
    echo "POSTGRES_TEST_USER=$POSTGRES_TEST_USER" > .env.test
    echo "POSTGRES_TEST_PASSWORD=$POSTGRES_TEST_PASSWORD" >> .env.test
    echo "POSTGRES_TEST_PORT=$POSTGRES_TEST_PORT" >> .env.test
    echo "POSTGRES_TEST_HOST=$POSTGRES_TEST_HOST" >> .env.test
    echo "POSTGRES_TEST_DB=$POSTGRES_TEST_DB" >> .env.test
    echo "TEST_DATABASE__SQL_ALCHEMY_CONN=$TEST_DATABASE__SQL_ALCHEMY_CONN" >> .env.test
}

export_variables() {
    set -a
    source .env.test
    set +a
}

write_variables
export_variables