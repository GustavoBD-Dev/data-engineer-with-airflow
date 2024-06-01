from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

from datetime import datetime


'''
Variable in Airflow
    Key: ml_model_parameters
    Val: {"param":[100,150,200]}
    Desc: machine learning parameters to try

    Key: ml_report_name
    Val: daily-report
    desc: 
'''

def _ml_task(ml_parameter):
    print(ml_parameter)

with DAG('ml_dag', start_date=datetime(2024, 6, 1),
    schedule_interval='@daily', catchup=False) as dag:

    ml_tasks = []

    for ml_parameter in Variable.get('ml_model_parameters', deserialize_json=True)["param"]:
        print(ml_parameter)
        ml_tasks.append(
            PythonOperator(
                task_id=f'ml_task_{ml_parameter}',
                python_callable=_ml_task,
                op_kwargs={
                    'ml_parameter':ml_parameter
                }
            )
        )
    
report = BashOperator(
    task_id='report',
    bash_command='echo "report_{{ var.value.ml_report_name }}"'
)
    
ml_tasks >> report
