FROM apache/airflow:3.3.1 AS airflow
COPY --chown=airflow:root pyproject.toml README.md ./
RUN mkdir -p src \
    && pip3 install --no-cache-dir .[airflow-backend-prod]
COPY --chown=airflow:root . .
RUN pip3 install --no-cache-dir --no-deps .


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS fastapi
WORKDIR /app
COPY pyproject.toml README.md ./
RUN mkdir -p src \
    && pip3 install --no-cache-dir .[fastapi-backend-prod]
COPY ./src/fastapi_routes /app
COPY . .
RUN pip3 install --no-cache-dir --no-deps .