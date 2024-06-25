SHELL:=/bin/bash
include .env

create_raw_tables: ## Create Postgres db and ddl for raw data
	psql -U postgres -d postgres -a -f capstone/gh_app/utils/create_gh_raw_tables.sql

docker_up: ## Start Docker
	@docker compose up -d

docker_down: ## Turn Docker down
	@docker compose down

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

ssh_connection: ## Airflow SSH connection
	@docker compose run airflow-cli airflow connections add ssh-conn \
	--conn-type=ssh --conn-host=spark-master \
	--conn-login=spark_user --conn-password=airflow \
	--conn-description "SSH Connection"


iceberg_commits: ## Test pyspark-iceberg consumer
	@docker exec -it spark-master spark-submit --master spark://spark-master:7077 --deploy-mode client ./kafka_consumer/pyspark_consume_from_kafka.py --topic commits

dbt_docs_generate: ## Generate dbt docs
	@docker exec -it airflow-scheduler /bin/bash -c "cd /opt/airflow/dags/dbt/gh_app && dbt docs generate"

dbt_copy_catalog: ## Copy dbt catalog locally
	@docker cp airflow-scheduler:/opt/airflow/dags/dbt/gh_app/target /tmp/

dbt_launch_doc: ## Run the dbt server locally. Port used 8000
	python -m http.server --directory /tmp/target

help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(filter-out .env, $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-45s\033[0m %s\n", $$1, $$2}'