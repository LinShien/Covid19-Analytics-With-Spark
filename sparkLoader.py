# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:02:19 2020

@author: Lin_Shien
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
from pyspark.sql import functions
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

    def extract(self, dataset):
        datasetExtracted = self.filterUnusedColumns(dataset)
        datasetCastedToNumeric = self.castColumnsAsType(datasetExtracted)

        datasetCastedToNumeric.cache()

        self.extractLatestReportDate(datasetCastedToNumeric)
        casesAndDeathPerCountry = self.analyze(datasetCastedToNumeric)

        return casesAndDeathPerCountry

    @classmethod
    def filterUnusedColumns(cls, dataset):
        return dataset.selectExpr('CONTINENT_NAME as CONTINENT'
                , 'COUNTRY_SHORT_NAME as COUNTRY'
                , 'PEOPLE_DEATH_NEW_COUNT'
                , 'PEOPLE_POSITIVE_NEW_CASES_COUNT'
                , 'REPORT_DATE')

    @classmethod
    def castColumnsAsType(cls, dataset):
        return dataset.select('COUNTRY'
                , dataset.PEOPLE_DEATH_NEW_COUNT.cast('int').alias('DEATH_COUNT')
                , dataset.PEOPLE_POSITIVE_NEW_CASES_COUNT.cast('int').alias('CASES_COUNT')
                ,  to_date(dataset.REPORT_DATE, 'M/d/yyyy').alias('REPORT_DATE'))

    @classmethod
    def analyze(cls, dataset):
        return dataset.groupBy('COUNTRY')       \
                .sum('DEATH_COUNT', 'CASES_COUNT')      \
                .withColumnRenamed('sum(DEATH_COUNT)', 'TOTAL_DEAHT')       \
                .withColumnRenamed('sum(CASES_COUNT)', 'TOTAL_CASES')       \
                .orderBy('sum(CASES_COUNT)', ascending = False)

    def extractLatestReportDate(self, dataset):
        record = self.extractLatestReportDateFromTable(dataset)
        self.latestReportDate = record[0]['max(REPORT_DATE)']

    @classmethod
    def extractLatestReportDateFromTable(cls, dataset):
        return dataset.agg(functions.max(dataset.REPORT_DATE)).collect()

if __name__ == '__main__':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

    sparkLoader.buildSparkSession()

    loader = sparkLoader()
    covid19Dataset = sparkLoader.loadFile('/home/size7311/Covid19-Analytics-With-Spark/data/COVID-19 Activity.csv')
    transformedDataset = loader.extract(covid19Dataset)
    transformedDataset.toPandas().to_csv('Analytics_' + loader.latestReportDate.strftime('%m-%d-%Y') +  '.csv')
