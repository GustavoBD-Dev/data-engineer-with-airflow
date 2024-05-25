import json
import pathlib

import airflow
import airflow.utils
import airflow.utils.dates
import requests
import requests.exceptions as request_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(                                          # Instanciate a DAF object, this is the starting point of any workflow
    dag_id="download_rocket_lainches",              # name of the DAG (Displayed in the Airflow Interface IU)
    start_date=airflow.utils.dates.days_ago(14),    # The date at which the DAG should first start running
    schedule_interval=None                          # At what interval the DAG should run
)

dowload_launches = BashOperator(                    # Apply Bash to download the URL response with curl
    task_id="download_launches",                    # Tha name of the task
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag 
)

def _get_pictures(): # A Python function will parse the response and download all rocket pictures 
    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f: # Open the rocket launches´ JSON
        launches = json.load(f) # Read as a dict so we can mingle the data 
        # For every launch, fetch element "image"
        image_urls = [launch["image"] for launch in launches["results"]] 

        # Loop over all image URL´s.
        for image_url in image_urls:
            try:
                response = requests.get(image_url) # Get the image
                # Get the only filename by selecting everything after the last.
                image_filename = image_url.split("/")[-1]
                # construct the target file path
                target_file = f"/tmp/images/{image_filename}"
                # Open target to file path
                with open(target_file, "wb") as f:
                    # write the image to file path
                    f.write(response.content)
                # Print result
                print(f"Downloaded {image_url} to {target_file}")
            # Catch and procces potential error 
            except request_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except request_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

    
# Call the Python function in the DAG with a PythonOperator
get_pictures = PythonOperator(
    task_id = "get_pictures", # name of the task
    python_callable=_get_pictures,  
    dag=dag  # Reference to the variable DAG
)

notify = BashOperator(
    task_id = "notify", # name of the task
    bash_command='echo "There are now $(ls /tmp/images | wc -l) images."',
    dag=dag # reference to the variable DAG
)

# Set the order of execution of tasks
dowload_launches >> get_pictures >> notify
