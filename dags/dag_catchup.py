from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Eu-Bitwise',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_catchup',
    default_args=default_args,
    description='dag with catchup',
    start_date=datetime(2023, 2, 20),
    schedule_interval='@daily',
    # Catchup or backfill will schedule  and execute all the missed runs up to the current time. 
    catchup=True
) as dag: 
    task1 = BashOperator(
        task_id='task1',
        bash_command="echo This is a simple bash command"
    )