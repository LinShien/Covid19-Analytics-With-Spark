# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:19 2020

@author: Lin_Shien
"""
from pyspark.sql import SparkSession
import sys

class sparkLoader(object):
    sparkSession = None
          
    @classmethod
    def buildSparkSession(cls):
        global sparkSession
        sparkSession = SparkSession.builder.config('spark.sql.warehouse.dir','file:///home/size7311/Covid19-Analytics-With-Spark').master('local[4]').appName("convid19Analytics").getOrCreate()
    
    @classmethod
    def loadFile(cls, filePath):
        return sparkSession.read.csv(filePath, header = True)
    
    @classmethod
    def transformDataset(cls, dataset):
        dataset = dataset.selectExpr('CONTINENT_NAME as CONTINENT', 'COUNTRY_SHORT_NAME as COUNTRY', 'PEOPLE_DEATH_NEW_COUNT', 'PEOPLE_POSITIVE_NEW_CASES_COUNT', 'REPORT_DATE')
        dataset = dataset.select('COUNTRY', dataset.PEOPLE_DEATH_NEW_COUNT.cast('int'), dataset.PEOPLE_POSITIVE_NEW_CASES_COUNT.cast('int'))
        dataset.cache()
        
        casesPerCountry = dataset.groupBy('COUNTRY').sum('PEOPLE_POSITIVE_NEW_CASES_COUNT', 'PEOPLE_DEATH_NEW_COUNT').orderBy('sum(PEOPLE_POSITIVE_NEW_CASES_COUNT)', ascending = False)
        
        return casesPerCountry
        
if __name__ == '__main__':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
    
    sparkLoader.buildSparkSession()
    covid19Dataset = sparkLoader.loadFile('/home/size7311/Covid19-Analytics-With-Spark/data/COVID-19 Activity.csv')
    transformedDataset = sparkLoader.transformDataset(covid19Dataset)
    
    transformedDataset.toPandas().to_csv('results.csv')
    

    
