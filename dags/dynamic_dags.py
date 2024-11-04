import sys
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from include.config.config import DAG_CONFIGS

# Load the DAG configurations from config.py
dag_configs = DAG_CONFIGS

# Function to create a task based on operator type and parameters
def create_task(dag, task_config):
    operator_class = task_config["operator"]
    task_id = task_config["task_id"]
    params = task_config["params"]

    # Instantiate the operator with task_id and params
    return operator_class(task_id=task_id, dag=dag, **params)

# Dynamically create DAGs based on the configuration file
for config in dag_configs:
    dag_id = config["dag_id"]
    schedule = config["schedule"]
    default_args = config.get("default_args", {})
    tasks = config["tasks"]
    dependencies = config.get("dependencies", [])

    # Create a new DAG for each entry in the config
    dag = DAG(dag_id=dag_id, default_args=default_args, schedule_interval=schedule)

    # Dictionary to hold tasks for setting dependencies later
    task_dict = {}

    # Create tasks and add them to the task dictionary
    for task_config in tasks:
        task = create_task(dag, task_config)
        task_dict[task.task_id] = task

    # Set dependencies based on the configuration
    for dependency in dependencies:
        upstream_task, downstream_task = dependency
        if upstream_task in task_dict and downstream_task in task_dict:
            task_dict[upstream_task] >> task_dict[downstream_task]
        else:
            raise ValueError(f"Dependency error: {upstream_task} or {downstream_task} not found in tasks.")

    # Register each dynamically created DAG in the globals
    globals()[dag_id] = dag
