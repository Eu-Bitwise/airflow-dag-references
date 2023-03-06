from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Eu-Bitwise',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_bashOperator',
    default_args=default_args,
    description='exec a few bash tasks',
    start_date=datetime(2023, 3, 1),
    schedule_interval='@daily'
) as dag: 
        task1 = BashOperator(
            task_id='first_task',
            bash_command="echo I was executed first!"
        )
        task2 = BashOperator(
            task_id='second_task',
            bash_command="echo I was executed after first task!"
        )
        task3 = BashOperator(
            task_id='third_task',
            bash_command="echo I was executed after first task!"
        )
        
        # task1.set_downstream(task2)
        # task1.set_downstream(task3)
        task1 >> [task2, task3]