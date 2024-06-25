"""
Query to the GitHub REST API for various endpoint
events
"""
from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable
from datetime import datetime, timedelta, timezone
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.bash_operator import (
    BashOperator
)

from airflow.operators.python import (
    BranchPythonOperator
)
from airflow.operators.dummy import (
    DummyOperator
)
from airflow.operators.trigger_dagrun import (
    TriggerDagRunOperator
)
from utils.process_gh_repo_requests import generate_concurrent_requests

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
    "max_active_runs": 1
}
dag = DAG(
    'gh_rest_commits_api',
    default_args=default_args,
    description="Task queries GitHub REST API endpoint - commits",
    schedule_interval="@hourly",
    start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)


run_date = "{{ dag_run.conf['execution_date'] if dag_run and dag_run.conf and 'execution_date' in dag_run.conf else ds_nodash }}"

fetch_commits = PythonOperator(
    task_id="fetch_commits",
    python_callable=generate_concurrent_requests,
    op_args=["commits"],
    dag=dag
)

# all_success = DummyOperator(
#         task_id='all_task_success',
#         dag=dag,
#         trigger_rule=TriggerRule.ALL_SUCCESS,
# )

trigger_kafka_commits_producer = TriggerDagRunOperator(
    task_id="trigger_kafka_commits_producer",
    trigger_dag_id="publish_commits_to_kafka",
    dag=dag
)

fetch_commits >> trigger_kafka_commits_producer