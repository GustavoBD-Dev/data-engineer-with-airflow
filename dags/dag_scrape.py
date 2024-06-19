from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from scrape import scrape_tools
import pendulum

with DAG(
    "scrape_tools",
    schedule=None,
    start_date=pendulum.datetime(2024, 5, 1),
    catchup=False
):
    scrape_tools_task = PythonOperator(
        task_id = 'scrape_tools',
        python_callable=scrape_tools
    )