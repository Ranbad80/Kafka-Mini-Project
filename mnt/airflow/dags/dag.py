from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import date, datetime, timedelta

import yfinance as yf
import pandas as pd




default_args = {
    "owner": "airflow",
    "start_date": datetime.today() - timedelta(days=1),
    "retries": 2,  # retry twice
    "retry_delay": timedelta(minutes=5)  # five minutes interval
}

today = date.today()
LOCAL_DIR = 'tmp/data/' + str(today)

def download_stock(symbol):
    start_date = today
    end_date = start_date + timedelta(days=1)
    df = yf.download(symbol, start=start_date, end=end_date, interval='1m')
    df.to_csv(symbol + '_data.csv', header=True)


def query_stock():
    apple_data = pd.read_csv(
        LOCAL_DIR + "/AAPL_data.csv").sort_values(by="Datetime", ascending=False)
    tesla_data = pd.read_csv(
        LOCAL_DIR + "/TSLA_data.csv").sort_values(by="Datetime", ascending=False)
    spread = [apple_data['High'][0] - apple_data['Low']
              [0], tesla_data['High'][0] - tesla_data['Low'][0]]
    return spread



with DAG(dag_id="marketvol",
         schedule_interval="0 18 * * 1-5",  # running at 6pm for weekdays
         default_args=default_args,
         description='source Apple and Tesla data' ) as dag:

    task_0 = BashOperator(
        task_id="make_datafolder",
        bash_command='''mkdir -p $AIRFLOW_HOME/tmp/data/''' +
        str(date.today())  # naming the folder with the current day
    )

    # extract data for symbol AAPL
    t1 = PythonOperator(
    task_id='download_appledata',
    dag=dag,
    python_callable=download_stock,
    op_kwargs={'symbol': 'AAPL'}
    )

    t2 = PythonOperator(
        task_id='download_tesladata',
        dag=dag,
        python_callable=download_stock,
        op_kwargs={'symbol': 'TSLA'}
    )

    # move data download into a same place
    t3 = BashOperator(
        task_id='move_appledata',
        dag=dag,
        bash_command='mv $AIRFLOW_HOME/AAPL_data.csv $AIRFLOW_HOME/tmp/data/' +
        str(today) + "/"
    )

    t4 = BashOperator(
        task_id='move_tesladata',
        dag=dag,
        bash_command='mv $AIRFLOW_HOME/TSLA_data.csv $AIRFLOW_HOME/tmp/data/' + str(today) + "/")

    t5 = PythonOperator(
        task_id="query_stock",
         python_callable=query_stock,
         dag=dag
        )

task_0 >> [t1, t2]
t1 >> t3
t2 >> t4
[t3, t4] >> t5


