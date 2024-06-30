from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'retry':5,
    'retry_delay':timedelta(minutes=5)

}

with DAG(dag_id='simple_dag', 
        start_date=days_ago(3),
        catchup=False, 
        default_args=default_args, # agrs into task_#
        # max_active_runs=2, # maximun number of DAG runs for specific DAG
        schedule_interval="@daily") as dag:
        # schedule_interval=None) as dag:
        # schedule_interval=timedelta(days=1)) as dag:

    task_1 = DummyOperator(
        task_id = 'task_1'
    )

    task_2 = DummyOperator(
        task_id = 'task_2'
    )

    task_3 = DummyOperator(
        task_id = 'task_3'
    )