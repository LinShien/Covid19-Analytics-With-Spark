from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor

import pandas as pd

default_args = {
        'owner' : 'size7311',
        'depends_on_past' : False,
        'start_date' : datetime(2020, 1, 1),
        'schedule_interval' : '@daily'
}

download_command = '''
    cd ~/Covid19-Analytics-With-Spark/data
    wget -O "COVID-19 Activity.csv" '''

spark_command = '''
    cd ~/Covid19-Analytics-With-Spark
    spark-submit sparkLoader.py
'''

rawDataRename_command = '''
    cd ~/Covid19-Analytics-With-Spark/data
    mv "COVID-19 Activity.csv" "COVID-19 Activity-$(date +%Y-%m-%d).csv"
'''
    
with DAG('dag_for_spark', catchup = False, default_args = default_args) as dag:
    downloadDataTask = BashOperator(
	    task_id = 'download_data_task',
	    bash_command = download_command + Variable.get('covid19_data_url')
	    )

    checkDataExists = FileSensor(
	    task_id = 'check_data_task',
	    filepath = '/home/size7311/Covid19-Analytics-With-Spark/data/COVID-19 Activity.csv',
	    poke_interval = 10,
	    timeout = 100
	    )

    sparkTask = BashOperator(
            task_id = 'spark_task',
            bash_command = spark_command
            )

    dataRenameTask = BashOperator(
	    task_id = 'data_rename_task',
	    bash_command = rawDataRename_command
	    )

    downloadDataTask >> checkDataExists >> sparkTask >> dataRenameTask
