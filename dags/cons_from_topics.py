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


# database related
host = "melachallengedatabase.crlafpfc5g5y.us-east-1.rds.amazonaws.com"
db = "changdb"
port = "5432"
user = "changuser"
passw = "changpass"


# define the DAG

etl_dag = DAG(
    'cons.backtests.Kafka.X.postgresql',
    default_args=default_args,
    start_date=datetime(2022, 10, 11),
    description='An end to end data pipeline for week 8 of 10 academy project',
    schedule=timedelta(hours=10),  # run every given time
    catchup=False                    # dont perform a backfill of missing runs
)

# endregion


# region consume scene

def consume_scene():
    print('consuming scenes. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(SCENES_TOPIC,
                             group_id='base-development-group-scenes',
                             bootstrap_servers=aws_instance_bootstrap_servers,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        # decoded_data = json.dumps(msg, indent=4, ensure_ascii=False)
        decoded_data = msg.value.decode("utf-8")
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
    print('consuming scenes completed. . .')


subscribe_to_scene = PythonOperator(
    task_id='subscribe_to_scene',
    python_callable=consume_scene,
    dag=etl_dag
)


def consume_result():
    print('consuming results. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(RESULTS_TOPIC,
                             group_id='base-development-group-results',
                             bootstrap_servers=aws_instance_bootstrap_servers,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        # decoded_data = json.dumps(msg, indent=4, ensure_ascii=False)
        decoded_data = msg.value.decode("utf-8")
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
    print('consuming results completed. . .')


subscribe_to_result = PythonOperator(
    task_id='subscribe_to_result',
    python_callable=consume_result,
    dag=etl_dag
)


def consume_ml_result():
    print('consuming ml results. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(RESULTS_TOPIC_ML,
                             group_id='base-development-group-ml-results',
                             bootstrap_servers=aws_instance_bootstrap_servers,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        # decoded_data = json.dumps(msg, indent=4, ensure_ascii=False)
        decoded_data = msg.value.decode("utf-8")
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
    print('consuming results completed. . .')


subscribe_to_ml_result = PythonOperator(
    task_id='subscribe_to_ml_result',
    python_callable=consume_ml_result,
    dag=etl_dag
)


# endregion


# region transformations

def transform():
    print('making several transformation . . .')
    print('making several transformations completed. . .')


make_transformations = PythonOperator(
    task_id='make_transformations',
    python_callable=transform,
    dag=etl_dag
)

# endregion


# region insertions

def load_to_scenes_table():
    print('loading scene into db. . .')
    # engine = create_engine(f'postgresql://{user}@{host}/{db}')
    engine = create_engine(
        f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

    select_users_query = """
        SELECT *
        FROM public.users
        ORDER BY users.id;
    """

    with engine.connect() as conn:
        # query = text("Show table")
        a = conn.execute(select_users_query)
        print(a.fetchall())

    print('loading scene into db completed. . .')


load_scene_to_db = PythonOperator(
    task_id='load_scene_to_db',
    python_callable=load_to_scenes_table,
    dag=etl_dag
)


def load_to_results_table():
    print('loading back test results into db. . .')

    # engine = create_engine(f'postgresql://{user}@{host}/{db}')
    engine = create_engine(
        f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

    select_users_query = """
        SELECT *
        FROM public.users
        ORDER BY users.id;
    """

    with engine.connect() as conn:
        # query = text("Show table")
        a = conn.execute(select_users_query)
        print(a.fetchall())

    print('loading back test results into  db completed. . .')


load_results_to_db = PythonOperator(
    task_id='load_results_to_db',
    python_callable=load_to_results_table,
    dag=etl_dag
)


def load_to_ml_results_table():
    print('loading ml results into db. . .')

    # engine = create_engine(f'postgresql://{user}@{host}/{db}')
    engine = create_engine(
        f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

    select_users_query = """
        SELECT *
        FROM public.users
        ORDER BY users.id;
    """

    with engine.connect() as conn:
        # query = text("Show table")
        a = conn.execute(select_users_query)
        print(a.fetchall())

    print('loading ml results into  db completed. . .')


load_results_ml_to_db = PythonOperator(
    task_id='load_results_ml_to_db',
    python_callable=load_to_ml_results_table,
    dag=etl_dag
)

# endregion


# run tasks in the dag
[subscribe_to_scene, subscribe_to_result, subscribe_to_ml_result] >> make_transformations >> [
    load_scene_to_db, load_results_to_db, load_results_ml_to_db]
