from datetime import datetime, timedelta, date
from multiprocessing import Value
from airflow import DAG
from airflow.models.dag import dag
from airflow.models.taskinstance import Context
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pathlib import Path

file_list = Path("/opt/airflow/logs/marketvol") .rglob('*.log')


def analyze_file(file,symbol):
    count=0
    list_error=[]
    logfile_list = [file_list]
    for file in logfile_list:
        
        str_file=str(file)
        if symbol in str_file:
            log_file = open(str_file, "r")
            for line in log_file:
                if 'ERROR' in line:
                    count+=1
                    list_error.append(line)
    Context["ti"].xcom_push(key="count",Value=count,
                            key="list_error", value=list_error)
    print('Total number of errors:'+str(count) )
    print('Here are all the errors:'+ str(list_error))

default_args={
    'owner': "airflow",
    'start_date':datetime.today()
}

with DAG(
    dag_id = "log_analyzer",
    default_args=default_args,
    schedule_interval = "* * * * *"  # Formerly used "@daily".
         ) as dag:
    
    t1=PythonOperator(
        task_id='AAPL_ERRORlog',
        python_callable=analyze_file,
        op_kwargs={"file": "file_list", "symbol": "AAPL"}
    )
    t2 = PythonOperator(
        task_id='TSLA_ERRORlog',
        python_callable=analyze_file,
        op_kwargs={"file": "file_list", "symbol": "TSLA"}
    )

if __name__ == '__main__':
    analyze_file(file_list, "AAPL")

t1>>t2
