from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Eu-Bitwise',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')

    print(f"Hello world! My name is {first_name} {last_name}, "
          f"and my age is {age}")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry')
    ti.xcom_push(key='last_name', value='Freeman')

def get_age(ti):
    ti.xcom_push(key='age', value=18)

with DAG(
    dag_id='dag_pythonOperator',
    default_args=default_args,
    description='DAG using python opearators',
    start_date=datetime(2023, 3, 1),
    schedule_interval='@daily'
) as dag: 
        task1 = PythonOperator(
            task_id='greet',
            python_callable=greet,
        )
        task2 = PythonOperator(
            task_id='get_name',
            python_callable=get_name,
        )
        task3 = PythonOperator(
            task_id='get_age',
            python_callable=get_age,
        )
        
        [task2, task3] >> task1