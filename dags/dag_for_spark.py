from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd

default_args = {
        'owner' : 'size7311',
        'depends_on_past' : False,
        'start_date' : datetime(2020, 1, 1),
        'schedule_interval' : '@daily'
}

bash_command = '''
    cd ~/Covid19-Analytics-With-Spark
    spark-submit sparkLoader.py
'''

def readSparkResults(**context):
    dataframe = pd.read_csv('/home/size7311/Covid19-Analytics-With-Spark/results.csv')

    pd.set_option('display.max_rows', dataframe.shape[0] + 1)

    print(dataframe)


with DAG('dag_for_spark', catchup = False, default_args = default_args) as dag:
    sparkOperator = BashOperator(
            task_id = 'spark_task',
            bash_command = bash_command,
            )
    
    pandasOperator = PythonOperator(
	    task_id = 'pandas_task',
   	    python_callable = readSparkResults,
    )

    sparkOperator >> pandasOperator
	    

