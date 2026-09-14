FROM apache/airflow:3.3.1 AS airflow
COPY --chown=airflow:root . .
RUN pip3 install --no-cache-dir .[dev]

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS fastapi
WORKDIR /app
COPY ./src/fastapi /app