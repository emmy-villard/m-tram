FROM apache/airflow:3.3.1
COPY requirements/dev.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY scripts/prod scripts