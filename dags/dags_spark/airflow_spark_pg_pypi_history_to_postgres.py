"""
Fetch pg tables and write them to iceberg
"""
import os
from datetime import datetime, timedelta
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
logger = logging.getLogger(__name__)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
    "max_active_runs": 1,
    "render_template_as_native_obj": True
}
dag = DAG(
    'publish_pg_raw_pypi_overall_to_iceberg',
    default_args=default_args,
    description="Task publishes pg raw tables pypi history to iceberg",
    schedule=None,
    # start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)


def extract_dates(**kwargs):
    dag_run = kwargs.get('dag_run')
    start_date = dag_run.conf.get('start_date') if dag_run and 'start_date' in dag_run.conf else ''
    end_date = dag_run.conf.get('end_date') if dag_run and 'end_date' in dag_run.conf else ''
    
    # Log dates
    logger.info(f'Start date {start_date}')
    logger.info(f'End date {end_date}')

    # Set default dates if they are not provided
    # today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # end_date = today - timedelta(1)
    # start_date = end_date - timedelta(180)
    if not start_date:
        start_date = datetime.now().replace(minute=0, second=0, microsecond=0)

    if not end_date:
        end_date = start_date + timedelta(hours=23, minutes=59, seconds=59, microseconds=0)

    # Format dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    # Return dates to be used by downstream tasks
    return {'start_date': f'{start_date_str}', 'end_date': f'{end_date_str}'}

extract_dates_task = PythonOperator(
    task_id='extract_dates',
    provide_context=True,
    python_callable=extract_dates,
    dag=dag
)

SSHHook = SSHHook(ssh_conn_id="ssh-conn", key_file="/home/airflow/.ssh/id_ecdsa", cmd_timeout=None)

templated_command = """
    export PYTHONPATH=/opt/spark:/opt/spark/kafka_consumer/:/opt/spark/utils/:$PYTHONPATH && 
    export BOOTSTRAP_SERVER={0} &&
    export POSTGRES_DB={1} &&
    export POSTGRES_USER={2} &&
    export POSTGRES_PASSWORD={3} &&
    export POSTGRES_PORT={4} &&
    export POSTGRES_HOST={5} &&
    export S3_LOCATION={6} &&
    export AWS_ACCESS_KEY_ID=minio &&
    export AWS_SECRET_ACCESS_KEY=minio123 &&
    export AWS_REGION=us-east-1 &&
    /opt/spark/bin/spark-submit --master spark://spark-master:7077 --deploy-mode client \
        /opt/spark/spark_batch/pg_to_iceberg.py \
            --table overall \
            --start_date '{{{{ ti.xcom_pull(task_ids='extract_dates')['start_date'] }}}}' \
            --end_date '{{{{ ti.xcom_pull(task_ids='extract_dates')['end_date'] }}}}'
""".format(
    os.getenv('BOOTSTRAP_SERVER'),
    os.getenv('POSTGRES_DB'),
    os.getenv('POSTGRES_USER'),
    os.getenv('POSTGRES_PASSWORD'),
    os.getenv('PORT'),
    os.getenv('POSTGRES_HOST'),
    os.getenv('S3_LOCATION')
)
spark_pypi_history_transfer = SSHOperator(
    task_id="spark_pypi_history_transfer",
    command=templated_command,
    ssh_hook=SSHHook,
    dag=dag
)

trigger_dbt_pypi_history_model = TriggerDagRunOperator(
    task_id="trigger_dbt_pypi_history_model",
    trigger_dag_id="pypi_app_overall_models",
    dag=dag
)

extract_dates_task >> spark_pypi_history_transfer >> trigger_dbt_pypi_history_model