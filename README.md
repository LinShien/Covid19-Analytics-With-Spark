# Covid19-Analytics-With-Spark
Use Apache Spark to analyze with covid 19 dataset

Data source from https://data.world/covid-19-data-resource-hub/covid-19-case-counts

***
## Requirements
* Ubuntu 18.04
* Python 3.6 >= 
* Apache Spark
* Apache Airflow
* Python3-pip

***
## Airflow Installation
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
###### Append the line below in .bashrc file
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
![img1](https://github.com/LinShien/Covid19-Analytics-With-Spark/blob/master/images/airflow_config.png)
