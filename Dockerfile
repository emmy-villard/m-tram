FROM apache/airflow:3.3.1
COPY requirements/dev.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY --chown=airflow:root . .
RUN pip3 install --no-deps .