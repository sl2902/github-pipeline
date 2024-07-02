SHELL:=/bin/bash
include .env

create_raw_tables: ## Create Postgres db and ddl for raw data
	psql -U postgres -d postgres -a -f capstone/gh_app/utils/create_gh_raw_tables.sql

docker_build: ## Build Docker containers
	@docker compose build --no-cache

docker_up: ## Start Docker
	@docker compose up -d

docker_down: ## Stop Docker
	@docker compose down

dag_list: ## List DAGs
	@docker-compose run airflow-cli airflow dags list

dag_run_base_repo_pipeline: ## Run base_repo pipeline
	@docker-compose run airflow-cli airflow tasks clear -y gh_rest_base_repo_api
	@docker-compose run airflow-cli airflow dags unpause gh_rest_base_repo_api
	@docker-compose run airflow-cli airflow dags unpause publish_pg_raw_base_repo_to_iceberg
	@docker-compose run airflow-cli airflow dags unpause gh_app_base_repo_models
	@docker-compose run airflow-cli airflow dags trigger gh_rest_base_repo_api
	@docker compose run airflow-cli airflow dags list-runs -d gh_rest_base_repo_api --state running

dag_run_commits_pipeline: ## Run commits pipeline
	@docker-compose run airflow-cli airflow tasks clear -y gh_rest_commits_api
	@docker-compose run airflow-cli airflow dags unpause gh_rest_commits_api
	@docker-compose run airflow-cli airflow dags unpause publish_pg_raw_commits_to_iceberg
	@docker-compose run airflow-cli airflow dags unpause gh_app_commits_models
	@docker-compose run airflow-cli airflow dags trigger gh_rest_commits_api
	@docker compose run airflow-cli airflow dags list-runs -d gh_rest_commits_api --state running


dag_run_issues_pipeline: ## Run issues pipeline
	@docker-compose run airflow-cli airflow tasks clear -y gh_rest_issues_api
	@docker-compose run airflow-cli airflow dags unpause gh_rest_issues_api
	@docker-compose run airflow-cli airflow dags unpause publish_pg_raw_issues_to_iceberg
	@docker-compose run airflow-cli airflow dags unpause gh_app_issues_models
	@docker-compose run airflow-cli airflow dags trigger gh_rest_issues_api
	@docker compose run airflow-cli airflow dags list-runs -d gh_rest_issues_api --state running

dag_run_overall_pipeline: ## Run pypi overall pipeline
	@docker-compose run airflow-cli airflow tasks clear -y gh_rest_pypi_overall_api
	@docker-compose run airflow-cli airflow dags unpause gh_rest_pypi_overall_api
	@docker-compose run airflow-cli airflow dags unpause publish_pg_raw_pypi_overall_to_iceberg
	@docker-compose run airflow-cli airflow dags unpause pypi_app_overall_models
	@docker-compose run airflow-cli airflow dags trigger gh_rest_pypi_overall_api
	@docker compose run airflow-cli airflow dags list-runs -d gh_rest_pypi_overall_api --state running


docker_clean: ## Clean Docker environment
	@docker images -aq | xargs -r docker rmi -f
	@docker volume ls -q| xargs -r docker volume rm
	@docker system prune -f
	@docker builder prune -f

list_kafka_topics: ## List Kafka topics
	@docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

consume_commits: ## Consume commits topic
	@docker exec -it kafka kafka-console-consumer \
	--bootstrap-server localhost:9092 --topic commits --from-beginning --max-messages 10

number_of_msg: ## Count number of messages in topic
	@docker exec capstone-project-sundeep-kafka-1 \
    kcat -b localhost:9092 -C -t pageviews -e -q | \
    wc -l

spark_connection: ## Airflow Spark Submit connection
	@docker compose run airflow-cli airflow connections add spark-conn \
	--conn-type=spark --conn-host=spark://spark-master:7077 \
	--conn-extra='{"queue": "root.default", "deploy-mode": "client"}' \
	--conn-description "Spark Default Connection"

ssh_conn: ## Airflow SSH connection
	@docker compose run airflow-cli airflow connections add ssh-conn \
	--conn-type=ssh --conn-host=spark-master \
	--conn-login=spark_user --conn-password=airflow \
	--conn-description "SSH Connection"

iceberg_batch_base_repo: ## Test spark batch data transfer - pg to iceberg for base_repo
	@docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./spark_batch/pg_to_iceberg.py --table base_repo --start_date "2024-06-30 16:00:00" --end_date "2024-06-30 17:00:00"

iceberg_batch_commits: ## Test spark batch data transfer - pg to iceberg
	@docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./spark_batch/pg_to_iceberg.py --table commits --start_date "2024-06-30 18:00:00" --end_date "2024-06-30 19:00:00"

iceberg_base_repo: ## Test pyspark-iceberg base_repo consumer
	@docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./kafka_consumer/pyspark_consume_from_kafka.py --topic commits

iceberg_commits: ## Test pyspark-iceberg commits consumer
	@docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./kafka_consumer/pyspark_consume_from_kafka.py --topic commits

dbt_docs_generate: ## Generate dbt docs
	@docker exec -it airflow-scheduler /bin/bash -c "cd /opt/airflow/dags/dbt/gh_app && dbt docs generate"

dbt_copy_catalog: ## Copy dbt catalog locally
	@docker cp airflow-scheduler:/opt/airflow/dags/dbt/gh_app/target /tmp/

dbt_launch_doc: ## Run the dbt server locally. Port used 8000
	python -m http.server --directory /tmp/target

help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(filter-out .env, $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-45s\033[0m %s\n", $$1, $$2}'