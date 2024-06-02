from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'backfill_trigger_dag',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    tags=['backfill-trigger-cli'],
    catchup=False
):
    # use the UI to trigger a DAG run with conf to trigger a backfill, passing in start/end dates and dag_id etc:
    trigger_backfill = BashOperator(
        task_id='trigger_backfill',
        bash_command="airflow dags backfill --reset-dagruns -y -s {{ dag_run.conf['date_start'] }} -e {{ dag_run.conf['date_end'] }} {{ dag_run.conf['dag_id'] }}"
    )

    trigger_backfill


