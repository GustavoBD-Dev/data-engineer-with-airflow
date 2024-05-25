from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from airflow.utils.helpers import chain
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


with DAG('load_file', start_date=datetime(2024, 5, 1), 
         description="DAG to check data", tags=['data_enginnering'],
         schedule='@daily', catchup=False):
    

    # create file dummy in the tmp directory
    create_file = BashOperator(
        task_id='create_file',
        bash_command='echo "Hi there!" >/tmp/dummy'
    )

    # verify that file exists in the directory tmp
    check_file = BashOperator(
        task_id='check_file',
        bash_command='test -f /tmp/dummy'
    )

    # read file with command Python
    read_file = PythonOperator(
        task_id='read_file',
        python_callable=lambda: print(open('/tmp/dummy', 'rb').read())
    )

    # define the dependences
    create_file >> check_file >> read_file
