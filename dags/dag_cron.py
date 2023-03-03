from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'ljeles',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_cron',
    default_args=default_args,
    description='dag with cron expression',
    start_date=datetime(2023, 2, 15),
    # https://crontab.guru/
    schedule_interval='0 3 * * mon,fri'
) as dag: 
        task1 = BashOperator(
            task_id='first_task',
            bash_command="echo dag with cron expression!"
        )
        task1