from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.hooks.S3_hook import S3Hook
from datetime import datetime


default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 10, 1),
}


def read_file(ti):
    hook = S3Hook()
    file_content = hook.read_key(key="test.csv", bucket_name="test")

    return file_content


def print_file(ti):
    data = ti.xcom_pull(task_ids="read_file")
    print(data)


with DAG(
    "sample_dag", schedule_interval=None, catchup=False, default_args=default_args
) as dag:
    t1 = PythonOperator(task_id="read_file", python_callable=read_file)
    t2 = PythonOperator(task_id="print_file", python_callable=print_file)
    t3 = S3ListOperator(task_id="s3_list", bucket="test")

    (t1 >> [t2, t3])
