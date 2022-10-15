# importing the required libraries
import json
from random import randrange
from symbol import parameters
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


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
server = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092',
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

def consume_scene(ti):
    print('consuming scenes. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(SCENES_TOPIC,
                             group_id='base-development-group-scenes',
                             bootstrap_servers=server,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    list_of_vals = []
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        decoded_data = json.loads(msg.value.decode("utf-8"))
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
        list_of_vals.append(decoded_data)
    # push the record for the transformation task
    ti.xcom_push(key='scene_record', value=list_of_vals)
    print('consuming scenes completed. . .')


subscribe_to_scene = PythonOperator(
    task_id='subscribe_to_scene',
    python_callable=consume_scene,
    dag=etl_dag
)


def consume_result(ti):
    print('consuming results. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(RESULTS_TOPIC,
                             group_id='base-development-group-results',
                             bootstrap_servers=server,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    list_of_vals = []
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        decoded_data = json.loads(msg.value.decode("utf-8"))
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
        list_of_vals.append(decoded_data)
    # push the record for the transformation task
    ti.xcom_push(key='result_record', value=list_of_vals)
    print('consuming results completed. . .')


subscribe_to_result = PythonOperator(
    task_id='subscribe_to_result',
    python_callable=consume_result,
    dag=etl_dag
)


def consume_ml_result(ti):
    print('consuming ml results. . .')
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(RESULTS_TOPIC_ML,
                             group_id='base-development-group-ml-results',
                             bootstrap_servers=server,
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             # StopIteration if no message after
                             consumer_timeout_ms=10000)
    list_of_vals = []
    for msg in consumer:
        print(f'message: {msg}')
        print(f"value: {msg.value}")
        print(f"topic: {msg.topic}")
        print(f"partition: {msg.partition}")
        print(f"offset: {msg.offset}")
        decoded_data = json.loads(msg.value.decode("utf-8"))
        print(f"decoded data: {decoded_data}\ntype: {type(decoded_data)}")
        list_of_vals.append(decoded_data)
    # push the record for the transformation task
    ti.xcom_push(key='', value=list_of_vals)
    print('consuming ml results completed. . .')


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


parameter_ids = []
# region insertions


def load_to_scenes_table(ti):
    print('loading scene into db. . .')
    scene_data = ti.xcom_pull(key='scene_record',
                              task_ids='subscribe_to_scene')
    print(f"scene data: {scene_data}\ntype: {type(scene_data)}")

    for record in scene_data:
        print(f"row: {record}\ntype: {type(record)}")
        print(f"asset: {record['asset']} == type: {type(record['asset'])}")
        print(f"cash: {record['cash']} === type: {type(record['cash'])}")
        print(f"strategy: {record['strategy']} === type: {type(record['strategy'])}")
        print(f"start_date: {record['start_date']} === type: {type(record['start_date'])}")
        print(f"end_date: {record['end_date']} === type: {type(record['end_date'])}")

    # creating the db engine
    engine = create_engine(
        f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

    # clear the list for new parameter ids
    parameter_ids.clear()
    for record in scene_data:
        insert_parameters_query = f"""
            INSERT INTO g1.parameters(asset, starting_money, strategy,
                                      start_date, end_date)
            VALUES ('{record["asset"]}', {float(record["cash"])},
                    '{record["strategy"]}', '{record["start_date"]}',
                    '{record["end_date"]}');
        """

        get_current_id_query = f"""
            SELECT id FROM g1.parameters p WHERE (p.asset = '{record["asset"]}'
                                  and p.starting_money = {float(record["cash"])}
                                  and p.strategy = '{record["strategy"]}'
                                  and p.start_date = '{record["start_date"]}'
                                  and p.end_date = '{record["end_date"]}')
                                  LIMIT 1;
        """
        with engine.connect() as conn:
            # insert record
            try:
                a = conn.execute(insert_parameters_query)
                print(a.fetchall())
            except Exception as e:
                print(e)

            # fetch record id
            try:
                curr_id = conn.execute(get_current_id_query)
                for row in curr_id:
                    parameter_ids.append(row["id"])
                    print(f'current id: {row["id"]}')
            except Exception as e:
                print(e)
    print(f'parameter ids: {parameter_ids}')
    ti.xcom_push(key='parameter_ids',
                 value=parameter_ids)
    print('loading scene into db completed. . .')


load_scene_to_db = PythonOperator(
    task_id='load_scene_to_db',
    python_callable=load_to_scenes_table,
    dag=etl_dag
)


def load_to_results_table(ti):
    print('loading back test results into db. . .')
    result_data = ti.xcom_pull(key='result_record',
                               task_ids='subscribe_to_result')
    print(f"results data: {result_data}\ntype: {type(result_data)}")

    for record in result_data:
        print(f"row: {record}\ntype: {type(record)}")
        print(f"sharpe_ratio: {record['sharpe_ratio']} == type: {type(record['sharpe_ratio'])}")
        print(f"return: {record['return']} === type: {type(record['return'])}")
        print(f"max_drawdown: {record['max_drawdown']} === type: {type(record['max_drawdown'])}")
        print(f"win_trade: {record['win_trade']} === type: {type(record['win_trade'])}")
        print(f"loss_trade: {record['loss_trade']} === type: {type(record['loss_trade'])}")
        print(f"total_trade: {record['total_trade']} === type: {type(record['total_trade'])}")
        print(f"start_portfolio: {record['start_portfolio']} === type: {type(record['start_portfolio'])}")
        print(f"final_portfolio: {record['final_portfolio']} === type: {type(record['final_portfolio'])}")

    # creating the db engine
    engine = create_engine(
        f'postgresql+psycopg2://{user}:{passw}@{host}:{port}/{db}')

    id_is_at = 0
    parameter_idz = ti.xcom_pull(key='parameter_ids',
                                 task_ids='load_scene_to_db')
    print(f'parameter ids: {parameter_idz}')
    print(f"current id: {parameter_idz[id_is_at]}\ncurrent index: {id_is_at}")
    for record in result_data:
        print(f"current id: {parameter_idz[id_is_at]}\ncurrent index: {id_is_at}")
        insert_parameters_query = f"""
            INSERT INTO g1.backtests_results(sharpe_ratio, return,
                                             max_drawdown, win_trade,
                                             loss_trade, total_trade,
                                             start_portfolio, final_portfolio,
                                             parameter_id)
            VALUES ({float(record["sharpe_ratio"])}, {float(record["return"])},
                    {float(record["max_drawdown"])}, {record["win_trade"]},
                    {record["loss_trade"]}, {record["total_trade"]},
                    {float(record["start_portfolio"])},
                    {float(record["final_portfolio"])},
                    {parameter_idz[id_is_at]});
        """
        with engine.connect() as conn:
            try:
                a = conn.execute(insert_parameters_query)
                id_is_at += 1
                print(a.fetchall())
            except Exception as e:
                print(e)
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

    insert_parameters_query = """
        SELECT *
        FROM public.users
        ORDER BY users.id;
    """

    with engine.connect() as conn:
        try:
            a = conn.execute(insert_parameters_query)
            print(a.fetchall())
        except Exception as e:
            print(e)

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
