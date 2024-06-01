from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum


# We are using the task instance object that is 'ti' to do an xcom push with a desired key name.
def _transform(ti):
    import requests
    resp = requests.get('https://swapi.dev/api/people/2').json()
    print(resp)
    my_character = {}
    my_character["height"] = int(resp["height"]) - 20
    my_character["mass"] = int(resp["mass"]) - 50
    my_character["hair_color"] = "black" if resp["hair_color"] == "blond" else "blond"
    my_character["eye_color"] = "hazel" if resp["eye_color"] == "blue" else "blue"
    my_character["gender"] = "female" if resp["gender"] == "main" else "female"
    ti.xcom_push("character_info", my_character)

def _transform2(ti):
    import requests
    resp = requests.get(f'https://swapi.dev/api/people/2').json()
    print(resp)
    my_character = {}
    my_character["height"] = int(resp["height"]) - 20
    my_character["mass"] = int(resp["mass"]) - 50
    my_character["hair_color"] = "black" if resp["hair_color"] == "blond" else "brow"
    my_character["eye_color"] = "hazel" if resp["eye_color"] == "blue" else "black"
    my_character["gender"] = "female" if resp["gender"] == "main" else "female"
    ti.xcom_push("character_info", my_character)


def _load(ti):  # pull XCOM values from multiples task instances, we add _transform2
    print(ti.xcom_pull(key = "character_info", task_ids = ['_transform', '_transform2']))

# We shall instantiable our DAG object, and create dependencies between our two tasks.
with DAG(
    "xcoms_demo_1",
    schedule=None,
    start_date=pendulum.datetime(2023, 3, 1),
    catchup=False
):
    t1 = PythonOperator(
        task_id = '_transform',
        python_callable = _transform
    )

    t2 = PythonOperator(
        task_id = 'load',
        python_callable = _load
    )

    t3 = PythonOperator(
        task_id = '_transform2',
        python_callable = _transform2
    )

    # t1 >> t2

    [t1,t3] >> t2
