# importing the required libraries
from cgi import test
import os
from random import randrange
from xmlrpc.client import DateTime
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text
import pandas as pd
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import sys


default_args = {
    # 'start_date': days_ago(5),
    'owner': 'f0x_tr0t',
    'depends_on_past': False,
    'email': ['fisseha.137@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'tags': ['week8', 'backtests, Kafka clusters']
}

# kafka node server
aws_instance_bootstrap_servers = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092',
                                  'b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092']

# topics
SCENES_TOPIC = 'g1-SCENES_TOPIC'
RESULTS_TOPIC = 'g1-RESULTS_TOPIC'
RESULTS_TOPIC_ML = 'g1-RESULTS_ML_TOPIC'


# define the DAG
etl_dag = DAG(
    'prod.backtests.Kafka.X.postgresql',
    default_args=default_args,
    start_date=datetime(2022, 10, 11),
    description='An end to end data pipeline for week 8 of 10 academy project',
    schedule=timedelta(hours=5),  # run every given time
    catchup=False                    # dont perform a backfill of missing runs
)


# region produce scene


def gerRandomTicker() -> str:
    tickers = ['MSFT', 'TSLA', 'RNDG', 'GGMU', 'KKSKU', 'BKR', 'TST']
    rand_ind = randrange(0, 7, 1)
    return tickers[rand_ind]


def produce_scene():
    print(f'publishing scenes to {SCENES_TOPIC}. . .')
    producer = KafkaProducer(bootstrap_servers=aws_instance_bootstrap_servers)

    # producer = KafkaProducer(
    #   value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    # producer.send(TEST_SCENE_TOPIC, {"text": raw_data['article'][0]})
    _id = randrange(1, 50000, 1)
    _start_date = datetime.now()
    _ticker = gerRandomTicker()

    test_scene = json.dumps({"id": _id, "start": str(_start_date),
                             "end": str(_start_date), "ticker": _ticker},
                            indent=4)

    print(f'test scene: {test_scene}\ntype: {type(test_scene)}')
    byte_encoded_data = bytes(f"{test_scene}", encoding='utf-8')
    print(f'byte encoded test scene: {byte_encoded_data}\ntype: ' +
          f'{type(byte_encoded_data)}')

    future = producer.send(SCENES_TOPIC, byte_encoded_data)
    producer.close()
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()
        pass
    # Successful result returns assigned partition and offset
    print(f"value: {record_metadata}")
    print(f"topic: {record_metadata.topic}")
    print(f"partition: {record_metadata.partition}")
    print(f"offset: {record_metadata.offset}")
    print('publishing scenes completed. . .')


publish_scene = PythonOperator(
    task_id='produce_scene',
    python_callable=produce_scene,
    dag=etl_dag
)

publish_scene
