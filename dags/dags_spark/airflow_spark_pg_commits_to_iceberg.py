"""
Fetch pg tables and write them to iceberg
"""
import os
from dotenv import load_dotenv
import logging
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
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import (
    SSHOperator
)

_ = load_dotenv()
logger = logging.getLogger("airflow.task")

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
    'publish_pg_raw_commits_to_iceberg',
    default_args=default_args,
    description="Task publishes pg raw tables commits to iceberg",
    schedule=None,
    # start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)


run_date = "{{ dag_run.conf['execution_date'] if dag_run and dag_run.conf and 'execution_date' in dag_run.conf else ds_nodash }}"



SSHHook = SSHHook(ssh_conn_id="ssh-conn", key_file="/home/airflow/.ssh/id_ecdsa", cmd_timeout=None)


spark_commits_transfer = SSHOperator(
    task_id="spark_commits_transfer",
    command=f"""
    export PYTHONPATH=/opt/spark:/opt/spark/kafka_consumer/:/opt/spark/utils/:$PYTHONPATH && 
    export BOOTSTRAP_SERVER={os.getenv('BOOTSTRAP_SERVER')} &&
    export POSTGRES_DB={os.getenv('POSTGRES_DB')} &&
    export POSTGRES_USER={os.getenv('POSTGRES_USER')} &&
    export POSTGRES_PASSWORD={os.getenv('POSTGRES_PASSWORD')} &&
    export POSTGRES_PORT={os.getenv('PORT')} &&
    export POSTGRES_HOST={os.getenv('POSTGRES_HOST')} &&
    export S3_LOCATION={os.getenv('S3_LOCATION')} &&
    export AWS_ACCESS_KEY_ID=minio &&
    export AWS_SECRET_ACCESS_KEY=minio123 &&
    export AWS_REGION=us-east-1 &&
    /opt/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/spark/spark_batch/pg_to_iceberg.py --table commits
    """,
    ssh_hook=SSHHook,
    dag=dag
)

trigger_dbt_commits_model = TriggerDagRunOperator(
    task_id="trigger_dbt_commits_model",
    trigger_dag_id="gh_app_commits_models",
    dag=dag
)

spark_commits_transfer >> trigger_dbt_commits_model