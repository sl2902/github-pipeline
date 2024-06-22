"""Consume GitHub events from subscribed topic"""
# from concurrent.futures import ThreadPoolExecutor
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from typing import Any, Optional, Dict, List, Tuple, Union
from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer


_ = load_dotenv()

kafka_config = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVER'),
    'group.id': 'group11',
    'auto.offset.reset': 'latest'
}

def create_consumer(kafka_config: Dict):
    # Define the DeserializingConsumer
    return DeserializingConsumer({
        "bootstrap.servers": kafka_config["bootstrap.servers"],
        "group.id": kafka_config["group.id"],
        "auto.offset.reset": kafka_config["auto.offset.reset"]
    })

def consume_messages(topic: str):
    consumer = create_consumer(kafka_config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1)
            if msg is None:
                continue
            if msg.error():
                print('Consumer error: {}'.format(msg.error()))
                continue
            msg_value = json.loads(msg.value().decode('utf8'))
            json_obj = json.dumps(msg_value, ensure_ascii=False)
            # print('Successfully consumed record with key {} and value {}'.format(msg.key(), msg.value()))
            print(json_obj)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages('commits')

