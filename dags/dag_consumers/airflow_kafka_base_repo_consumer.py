"""
Consume events published to various Kafka
topics
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
# from airflow.providers.apache.spark.operators.spark_submit import (
#     SparkSubmitOperator
# )
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.ssh.operators.ssh import (
    SSHOperator
)
from kafka_consumer.consume_from_kafka import consume_messages

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
    'consume_base_repo_from_kafka',
    default_args=default_args,
    description="Task consumes base_repo from Kafka",
    schedule_interval=None,
    # start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)


run_date = "{{ dag_run.conf['execution_date'] if dag_run and dag_run.conf and 'execution_date' in dag_run.conf else ds_nodash }}"

# kafka_commits_consumer = PythonOperator(
#     task_id="kafka_commits_consumer",
#     python_callable=consume_messages,
#     op_args=["commits"],
#     dag=dag
# )

# kafka_issues_consumer = PythonOperator(
#     task_id="kafka_issues_consumer",
#     python_callable=consume_messages,
#     op_args=["issues"],
#     dag=dag
# )


SSHHook = SSHHook(ssh_conn_id="ssh-conn", key_file="/home/airflow/.ssh/id_ecdsa", cmd_timeout=None)


kafka_base_repo_consumer = SSHOperator(
    task_id="kafka_base_repo_consumer",
    # ssh_conn_id="ssh-conn",
    command=f"""
    export PYTHONPATH=/opt/spark:/opt/spark/kafka_consumer/:/opt/spark/utils/:$PYTHONPATH && 
    export BOOTSTRAP_SERVER={os.getenv('BOOTSTRAP_SERVER')} &&
    export AWS_ACCESS_KEY_ID=minio &&
    export AWS_SECRET_ACCESS_KEY=minio123 &&
    export AWS_REGION=us-east-1 &&
    /opt/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client /opt/spark/kafka_consumer/pyspark_consume_from_kafka.py --topic base_repo
    """,
    ssh_hook=SSHHook,
    dag=dag
)

trigger_dbt_base_repo_model = TriggerDagRunOperator(
    task_id="trigger_dbt_base_repo_model",
    trigger_dag_id="gh_app_base_repo_models",
    dag=dag
)

kafka_base_repo_consumer >> trigger_dbt_base_repo_model