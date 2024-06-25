"""
Publish events to Kafka topics
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
from kafka_producer.publish_to_kafka import publish_to_kafka

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
    'publish_base_repo_to_kafka',
    default_args=default_args,
    description="Task publishes base_repo to Kafka",
    schedule_interval=None,
    # start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)


run_date = "{{ dag_run.conf['execution_date'] if dag_run and dag_run.conf and 'execution_date' in dag_run.conf else ds_nodash }}"


kafka_base_repo_producer = PythonOperator(
    task_id="kafka_base_repo_producer",
    python_callable=publish_to_kafka,
    op_args=["/"],
    dag=dag
)

trigger_kafka_base_repo_consumer = TriggerDagRunOperator(
    task_id="trigger_kafka_base_repo_consumer",
    trigger_dag_id="consume_base_repo_from_kafka",
    dag=dag
)

kafka_base_repo_producer >> trigger_kafka_base_repo_consumer