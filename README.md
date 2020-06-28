# Covid19-Analytics-With-Spark
Use Apache Spark to analyze with covid 19 dataset

Data source from https://data.world/covid-19-data-resource-hub/covid-19-case-counts

<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/Analytics_demo.png" width="1000" height="700">

***
## Requirements
* Ubuntu 18.04
* Python 3.6 >= 
* Apache Spark 3.0.0
* Apache Airflow 1.10.10
* Python3-pip

***
## 1.Airflow Installation
#### Install Database for Airflow (default is sqlite)
````bash
sudo apt-get install mysql-server
sudo apt-get isntall mysql-client
sudo apt-get install libmysqlclient-dev
````
#### Create database and user for Airflow in MySQL
###### Open MySQL command line
````shell
mysql -u root
````
###### Inside MySQL command line
````mysql
mysql> create database airflow default charset utf8 collate utf8_general_ci;
mysql> create user airflow@'localhost' identified by 'airflow';
mysql> grant all on airflow.* to airflow@'localhost';
mysql> flush privileges;
mysql> show set global explicit_defaults_for_timestamp=1;
````
#### Install Python3-pip
````Bash
sudo apt install python3-pip
sudo pip3 install --upgrade pip3
````
#### Set Up home and variable for Airflow
````bash
mkdir ~/airflow
````
###### Add global variables
````bash
vi ~/.bashrc 
````
###### Append the line below in .bashrc file and save
````shell
export AIRFLOW_HOME=~/airflow  
````
#### Install Airflow
````Bash
pip install "apache-airflow[mysql, slack, crypto]"
````
#### Initialize Airflow and change MySQL as Airflow backend database
````airflow
cd ~/airflow
airflow initdb
````
###### Change Airflow config
````
vi airflow.cfg
````

<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/airflow_config.png" width="750" height="300">

##### Initialize Airflow with new configuartion 
````airflow
airflow initdb
````
##### Create folder for dags program
````bash
mkdir ~/airflow/dags
````
##### Run Airflow webserver
````Bash
airflow webserver -p 8080
````
<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/airflow_webUI.png" width="750" height="300">

##### Open your web browser and type the command below to view webserver UI
````Bash
localhost:8080
````
<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/airflow_webUI2.png" width="750" height="300">




##### Open another terminal and type command below to oper scheduler
````
airflow scheduler
````
<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/airflow_scheduler.png" width="750" height="300">

## 2. Apache Spark Installation
#### Download Apache Spark
````Bash
mkdir ~/download

wget http://apache.stu.edu.tw/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz
tar zxvf spark-3.0.0-bin-hadoop2.7

mv spark-3.0.0-bin-hadoop2.7 spark
mv spark ~
````
#### Download JDK for Spark
Download jdk https://www.oracle.com/tw/java/technologies/javase-downloads.html
version 8 or 11 both compatible for Spark

#### Install pyspark
````Bash
pip3 install pyspark
````
#### Add global variables
````
vi ~/.bashrc 
````
###### Append the line below in .bashrc file and save
````
export SPARK_HOME='/your home directory/spark/'
export PYSPARK_PYTHON='/usr/bin/python3'
export JAVA_HOME='/your home directory/name of your downloaded jdk'
export PATH='$SPARK_HOME:PATH'
export PATH='$PYSPARK_PYTHON:PATH'
export PATH='$JAVA_HOME:PATH'
````
#### Now you are able to run pyspark now
````Bash
$>pyspark
````
<img src="https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/pyspark.png" width="750" height="300">

