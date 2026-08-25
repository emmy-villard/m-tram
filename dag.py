from airflow.sdk import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from etl.extract.fetch_api import fetch_api
from etl.extract.api_url import url_ligne

@dag(schedule=None, description="ETL new ligne data")
def etl_new_ligne_data():
    task_extract = PythonOperator(task_id="ligne_extract") #, fetch_api(url_ligne))
    task_transform = PythonOperator(task_id="ligne_transform")
    task_load = PythonOperator(task_id="ligne_load")
    task_extract >> task_transform >> task_load