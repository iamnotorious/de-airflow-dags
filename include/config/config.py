from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from airflow.utils.dates import days_ago

DAG_CONFIGS = [
    # Example 1: A simple DAG with EmptyOperator placeholders
    {
        "dag_id": "simple_empty_dag",
        "schedule": "0 8 * * *",
        "default_args": {
            "owner": "airflow",
            "start_date": days_ago(1),
            "retries": 1
        },
        "tasks": [
            {
                "task_id": "start_task",
                "operator": EmptyOperator,
                "params": {}
            },
            {
                "task_id": "processing_task",
                "operator": EmptyOperator,
                "params": {}
            },
            {
                "task_id": "end_task",
                "operator": EmptyOperator,
                "params": {}
            }
        ],
        "dependencies": [
            ["start_task", "processing_task"],
            ["processing_task", "end_task"]
        ]
    },

    # Example 2: A DAG with BashOperator and EmptyOperator
    {
        "dag_id": "bash_and_empty_dag",
        "schedule": "0 10 * * *",
        "default_args": {
            "owner": "airflow",
            "start_date": days_ago(2),
            "retries": 2
        },
        "tasks": [
            {
                "task_id": "initial_bash",
                "operator": BashOperator,
                "params": {
                    "bash_command": "echo 'Running initial bash command'"
                }
            },
            {
                "task_id": "intermediate_empty",
                "operator": EmptyOperator,
                "params": {}
            },
            {
                "task_id": "final_bash",
                "operator": BashOperator,
                "params": {
                    "bash_command": "echo 'Final bash command completed'"
                }
            }
        ],
        "dependencies": [
            ["initial_bash", "intermediate_empty"],
            ["intermediate_empty", "final_bash"]
        ]
    },

    # Example 3: A more complex DAG with Databricks and DbtCloud tasks
    {
        "dag_id": "databricks_and_dbt_dag",
        "schedule": "0 14 * * *",
        "default_args": {
            "owner": "airflow",
            "start_date": days_ago(3),
            "retries": 3
        },
        "tasks": [
            {
                "task_id": "start_empty",
                "operator": EmptyOperator,
                "params": {}
            },
            {
                "task_id": "databricks_task_1",
                "operator": DatabricksSubmitRunOperator,
                "params": {
                    "databricks_conn_id": "databricks_default",
                    "json": {
                        "job_id": "databricks_job_1"
                    }
                }
            },
            {
                "task_id": "dbt_task_1",
                "operator": DbtCloudRunJobOperator,
                "params": {
                    "dbt_cloud_conn_id": "dbt_cloud_default",
                    "job_id": 11111
                }
            },
            {
                "task_id": "databricks_task_2",
                "operator": DatabricksSubmitRunOperator,
                "params": {
                    "databricks_conn_id": "databricks_default",
                    "json": {
                        "job_id": "databricks_job_2"
                    }
                }
            },
            {
                "task_id": "dbt_task_2",
                "operator": DbtCloudRunJobOperator,
                "params": {
                    "dbt_cloud_conn_id": "dbt_cloud_default",
                    "job_id": 22222
                }
            },
            {
                "task_id": "end_empty",
                "operator": EmptyOperator,
                "params": {}
            }
        ],
        "dependencies": [
            ["start_empty", "databricks_task_1"],
            ["databricks_task_1", "dbt_task_1"],
            ["dbt_task_1", "databricks_task_2"],
            ["databricks_task_2", "dbt_task_2"],
            ["dbt_task_2", "end_empty"]
        ]
    },

    # Example 4: Complex dependencies with multiple operators
    {
        "dag_id": "complex_dependency_dag",
        "schedule": "0 16 * * *",
        "default_args": {
            "owner": "airflow",
            "start_date": days_ago(4),
            "retries": 1
        },
        "tasks": [
            {
                "task_id": "start_task",
                "operator": EmptyOperator,
                "params": {}
            },
            {
                "task_id": "bash_task",
                "operator": BashOperator,
                "params": {
                    "bash_command": "echo 'Executing bash task'"
                }
            },
            {
                "task_id": "databricks_task",
                "operator": DatabricksSubmitRunOperator,
                "params": {
                    "databricks_conn_id": "databricks_default",
                    "json": {
                        "job_id": "databricks_job_3"
                    }
                }
            },
            {
                "task_id": "dbt_task",
                "operator": DbtCloudRunJobOperator,
                "params": {
                    "dbt_cloud_conn_id": "dbt_cloud_default",
                    "job_id": 33333
                }
            },
            {
                "task_id": "final_task",
                "operator": EmptyOperator,
                "params": {}
            }
        ],
        "dependencies": [
            ["start_task", "bash_task"],
            ["bash_task", "databricks_task"],
            ["databricks_task", "dbt_task"],
            ["dbt_task", "final_task"]
        ]
    }
]
