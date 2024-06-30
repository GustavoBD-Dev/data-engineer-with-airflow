from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'retry':5,
    'retry_delay':timedelta(minutes=5)
}

def _downloading_data(**kwargs):
    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_data')

with DAG(dag_id='simple_dag', 
        start_date=days_ago(3),
        catchup=False, 
        default_args=default_args, # agrs into task_#
        # max_active_runs=2, # maximun number of DAG runs for specific DAG
        schedule_interval="@daily") as dag:
        # schedule_interval=None) as dag:
        # schedule_interval=timedelta(days=1)) as dag:

    downloading_data = PythonOperator(
        task_id = 'downloading_data',
        python_callable=_downloading_data
    )

    task_1 = DummyOperator(
        task_id = 'task_1'
    )

    waiting_for_data = FileSensor(
        task_id='waiting_for_data',
        fs_conn_id='fs_default', # ID of the connection
        filepath='my_file.txt',
        poke_interval=30 # want to check every 30 seconds
    )