from airflow import DAG
from datetime import datetime
from airflow.utils.helpers import chain
from airflow.operators.python import PythonOperator

# could be use 
# dag = dag(...)
# then used the next script arguments
# task_a = PythonOperator(task_id='task_a', python_callable=print_a, dag=dag)
def print_a():
    print('hi from task a')

def print_b():
    print('hi from task b')

def print_c():
    print('hi from task c')

def print_d():
    print('hi from task d')

def print_e():
    print('hi from task e')

default_args = {
    'retries': 3,
}

with DAG('my_dag', start_date=datetime(2023, 1 , 1), default_args=default_args,
         description='A simple tutorial DAG', tags=['data_science'],
         schedule='@daily', catchup=False):
    
    task_a = PythonOperator(task_id='task_a', python_callable=print_a, retries=3)
    task_b = PythonOperator(task_id='task_b', python_callable=print_b, retries=3)
    task_c = PythonOperator(task_id='task_c', python_callable=print_c, retries=3)
    task_d = PythonOperator(task_id='task_d', python_callable=print_d, retries=3)
    task_e = PythonOperator(task_id='task_e', python_callable=print_e, retries=3)

    chain(task_a, [task_b, task_c], [task_d, task_e])











