from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'ljeles',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_postgres',
    default_args=default_args,
    description='dag using postgres database',
    start_date=datetime(2023, 2, 15),
    schedule_interval='0 0 * * *'
) as dag: 
        task1 = PostgresOperator(
            task_id='create_postgres_table',
            postgres_conn_id='postgres_localhost',
            sql="""
                CREATE table IF NOT EXISTS dag_runs (
                    dt date,
                    dag_id CHARACTER VARYING,
                    PRIMARY KEY (dt, dag_id)
                )
            """
        )
        
        task2 = PostgresOperator(
            task_id='insert_postgres_table',
            postgres_conn_id='postgres_localhost',
            sql="""
                INSERT INTO dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
            """
        )
        
        # Delete previous record to avoid key duplication
        task3 = PostgresOperator(
            task_id='delete_postgres_table',
            postgres_conn_id='postgres_localhost',
            sql="""
                DELETE FROM dag_runs
                WHERE dt = '{{ ds }}' AND dag_id = '{{ dag.dag_id }}'
            """
        )
        
        task1 >> task3 >> task2
        