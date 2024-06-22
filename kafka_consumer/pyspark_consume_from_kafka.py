from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType
import os
import json
import argparse
from dotenv import load_dotenv
from utils.iceberg_kafka_keys import *
from kafka_consumer.pyspark_topic_schemas import *
from kafka_consumer.iceberg_tables import *

_ = load_dotenv()

s3_location = "s3a://lakehouse"
schema_qry = f"""
        create database if not exists gh;
"""

spark = (
        SparkSession
            .builder
            .appName("Subscribe to GitHub events")
            .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

kafka_options = {
    "kafka.bootstrap.servers": os.getenv("BOOTSTRAP_SERVER"),
    "subscribe":"",
    "startingOffsets": "earliest",
    "maxOffsetsPerTrigger": 5000
}

def read_stream(topic: str, schema: StructType):
    kafka_options["subscribe"] = topic
    print(kafka_options)
    return(
        spark
            .readStream
            .format("kafka")
            .options(**kafka_options)
            .load()
            .selectExpr("cast(value as string)")
            .select(from_json(col("value"), schema=schema).alias("data"))
            .select("data.*")
            # .withColumn("ca_date", to_date(col("commit_author_date")))
    )

def write_stream(
        df: DataFrame, 
        checkpoint_location: str,
        output_table: str, 
        partition_keys: List[str]):
    return (
        df
        .writeStream
        .format("iceberg")
        .trigger(processingTime="3 minutes")
        .option("fanout-enabled", "true")
        .option("checkpointLocation", checkpoint_location)
        .outputMode("append")
        .toTable(output_table)
    )

def consume_stream_pipeline(
        topic: str, 
        checkpoint_location: str,
        partition_keys: list,
        output_table: str,
        schema: StructType = spark_schemas
    ):
    # spark.sql(schema_qry)
    # print(ice_tables["commits"])
    # spark.sql(f"drop table if exists bronze.{topic};")
    spark.sql(ice_tables[f'{topic}'].format(os.path.join(s3_location, topic)))
    df = read_stream(topic, schema)

    # query = df.writeStream \
    # .format("console")\
    # .option("numRows", 20) \
    # .option("truncate", "true") \
    # .outputMode("append") \
    # .start()

    query = write_stream(df, checkpoint_location, output_table, partition_keys)
    
    query.awaitTermination(timeout=60*5)
    # query.stop()

def main(topic: str):
    consume_stream_pipeline(
        topic,
        f"{s3_location}/checkpoints/{topic}",
        topic_keys[f'{topic}']["partition_keys"],
        f"bronze.{topic}",
        spark_schemas[f'{topic}']
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pyspark application")
    parser.add_argument('--topic',
             required=True,
             help='Kafka topic to consume from')
    args = parser.parse_args()
    main(args.topic)


