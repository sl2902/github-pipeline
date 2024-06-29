from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import StructType
import pandas as pd
import os
import json
import argparse
import logging
from dotenv import load_dotenv
from utils.db_connection import make_db_connection
from utils.iceberg_kafka_keys import *
from utils.iceberg_tables import *
from utils.pg_upstream_queries import *

logger = logging.getLogger("airflow.task")

_ = load_dotenv()

spark = (
    SparkSession
            .builder
            .appName("Fetch data from pg db and load into iceberg")
            .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

def read_pg_table(qry: str) -> DataFrame:
    host = os.getenv("POSTGRES_HOST", "upstreamdb")
    port = os.getenv("PORT", "5432")
    db = os.getenv("POSTGRES_DB", "gh_raw_db")
    jdbc_url = f'jdbc:postgresql://{host}:{port}/{db}'
    connection_properties = {
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "driver": "org.postgresql.Driver",
    }
    return (
        spark
            .read
            .format("jdbc")
            .option("url", jdbc_url)
            .option("query", qry)
            # .option("fetchsize", 1000)
            .option("user", connection_properties["user"])
            .option("password", connection_properties["password"])
            .option("driver", connection_properties["driver"])
            .load()
        )

def write_iceberg_table( 
        df: pd.DataFrame, 
        output_table: str, 
        # partition_keys: List[str]
    ):
    (
        df
        .writeTo(output_table)
        .using("iceberg")
        .tableProperty("write.spark.fanout.enabled", "true")
        # .append()
        # .option("overwrite-mode", "dynamic")
        .overwritePartitions()
    )

def consume_batch_pipeline(
        table: str, 
        partition_keys: list,
        output_table: str
    ):
    batch_size, offset = 500, 0
    spark.sql(ice_tables[f'{table}'].format(os.path.join(os.getenv("S3_LOCATION"), table)))
    count = 0
    endpoint = "/" if table == "base_repo" else table 
    while True:
        qry = raw_qry_str[endpoint]
        qry += f"limit {batch_size} offset {offset}"
        qry = qry.replace(";", "")
        logger.info(qry)
        df = read_pg_table(qry)
        count += df.count()
        if df.count() == 0:
            break
        offset += batch_size
        write_iceberg_table(df, output_table)
        # print(f"Running count: {count}")
        # final_count = spark.read.format("iceberg").load(output_table).count()
        # print(f"Final total records in Iceberg table: {final_count}")
    logger.info(f'Number of records {count}')


def main(table: str):
    consume_batch_pipeline(
        table,
        # f"{os.getenv('S3_LOCATION')}/checkpoints/{table}",
        topic_keys[f'{table}']["partition_keys"],
        f"bronze.{table}"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pyspark application")
    parser.add_argument('--table',
             required=True,
             help='Iceberg table name')
    args = parser.parse_args()
    main(args.table)