FROM apache/airflow:3.3.1
COPY --chown=airflow:root . .
RUN pip3 install --no-cache-dir .[dev]