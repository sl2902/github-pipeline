"""Publish GitHub events to Kafka topic"""
from confluent_kafka import SerializingProducer, KafkaError, Message
import json
from json.decoder import JSONDecodeError
import os
from datetime import datetime, date
from dotenv import load_dotenv
import logging
from kafka_producer.query_upstream_db import query_upstream_db
from utils.iceberg_kafka_keys import *

logger = logging.getLogger("airflow.task")

_ = load_dotenv()

def create_producer():
    # Define the SerializingProducer
    producer = SerializingProducer({
        'bootstrap.servers': os.getenv('BOOTSTRAP_SERVER'),
    }) 
    logger.info(f"Kafka broker {os.getenv('BOOTSTRAP_SERVER')}")
    return producer

def delivery_report(err: KafkaError, msg: Message):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.

    """
    if err is not None:
        logger.error(f'Delivery failed for user record {msg.key()}: {err}')
        return
    
    logger.info(f'User record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def date_encoder(data):
    if isinstance(data, (datetime, date)):
        return data.isoformat()

def publish_to_kafka(endpoint: str):
    """Publish the upstream data to Kafka topic"""
    logger.info("Query the upstream db")
    arr = query_upstream_db(endpoint)
    logger.info("Done querying upstream db")
    logger.info(f"Message to publish {len(arr)}")
    counter = 0
    endpoint = "base_repo" if endpoint == "/" else endpoint
    producer = create_producer()
    id_key = topic_keys[endpoint]["primary_key"]
    for row in arr:
        # Create a dictionary from the row values
        try:
            value = json.dumps(row, default=date_encoder)
        except JSONDecodeError as e:
            logger.error(f"Failed to serialize Kafka message: {e}") 
            continue
        # Produce to Kafka
        # logger.info(f"Counter {counter}")
        producer.produce(topic=endpoint, key=str(json.loads(value)[id_key]).encode('utf8'), value=value, on_delivery=delivery_report)
        counter += 1
        # Flush every 1000 events
        if counter % 1000 == 0:
            logger.info("Ready to flush")
            producer.flush()
            logger.info(f"Published {counter} messages to Kafka topic")
    producer.flush()
    logger.info(f"Data successfully published to Kafka topic {endpoint}")

if __name__ == "__main__":
    publish_to_kafka("issues")
    