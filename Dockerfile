FROM apache/airflow:3.3.1 AS airflow
COPY --chown=airflow:root . .
RUN pip3 install --no-cache-dir .[airflow-backend-prod]

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS fastapi
WORKDIR /app
COPY ./src/fastapi_routes /app
COPY . .
RUN pip3 install --no-cache-dir .[fastapi-backend-prod]