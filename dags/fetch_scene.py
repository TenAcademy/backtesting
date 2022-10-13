# importing the required libraries
import os
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine
import pandas as pd
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
