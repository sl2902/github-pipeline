"""Build dbt models"""
import os
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta, timezone

DBT_CWD = os.environ.get("DBT_CWD", f"{os.getenv('AIRFLOW_HOME')}/dags/dbt")

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

@dag(
    default_args=default_args,
    description="Create base_repo models in Trino",
    schedule=None,
    # start_date=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0),
    tags=["dev"]
)
def pypi_app_overall_models():
    run_date = "{{ dag_run.conf['execution_date'] if dag_run and dag_run.conf and 'execution_date' in dag_run.conf else ds_nodash }}"

    run_dbt_deps = BashOperator(
        task_id="run_dbt_deps",
        bash_command="dbt deps",
        cwd=DBT_CWD
    )
    # runs models for all layers - bronze, silver and gold
    dbt_run_pypi_overall = BashOperator(
        task_id='dbt_run_pypi_overall',
        bash_command='dbt run -s path:models/pypi_overall/',
        cwd=DBT_CWD
    )

    (
        run_dbt_deps \
        >> dbt_run_pypi_overall
    )

pypi_app_overall_models()