from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import chain, cross_downstream
from datetime import datetime, timedelta

default_args = {
    'retry':5,
    'retry_delay':timedelta(minutes=5)
}

def _downloading_data(ti, **kwargs):
    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_data')
    ti.xcom_push(key='my_key', value=43) # create the values to the next dependencie
    # return 42

def _checking_data(ti):
    # ti receives the values of the previous task
    xcom = ti.xcom_pull(key='my_key', task_ids=['downloading_data'])
    print(xcom)

def _failure(context):
    print("On callback failure")
    print(context)

with DAG(dag_id='simple_dag', 
        start_date=days_ago(3),
        catchup=True, 
        default_args=default_args, # agrs into task_#
        # max_active_runs=2, # maximun number of DAG runs for specific DAG
        schedule_interval="@daily") as dag:
        # schedule_interval=None) as dag:
        # schedule_interval=timedelta(days=1)) as dag:

    downloading_data = PythonOperator(
        task_id = 'downloading_data',
        python_callable=_downloading_data
    )

    # task_1 = DummyOperator(
    #     task_id = 'task_1'
    # )

    checking_data = PythonOperator(
        task_id = 'checking_data',
        python_callable=_checking_data
    )

    waiting_for_data = FileSensor(
        task_id='waiting_for_data',
        fs_conn_id='fs_default', # ID of the connection
        filepath='my_file.txt',
        poke_interval=30 # want to check every 30 seconds
    )

    processing_data = BashOperator(
        task_id = 'processing_data',
        bash_command='exit 1',
        on_failure_callback=_failure
    )

    # TASK DEPENDENCIES

    # lineal dependencies
    downloading_data >> checking_data >> processing_data >> waiting_for_data
    # with chain
    # chain(downloading_data , waiting_for_data , processing_data)
    
    # One task with two or more task dependencies
    # downloading_data >> [waiting_for_data , processing_data]

    # cross dependencies
    # task1 -> task_3
    #       -> task_4
    # task2 -> task_3
    #       -> task_4
    # cross_downstream([downloading_data, checking_data], [waiting_for_data, processing_data])
