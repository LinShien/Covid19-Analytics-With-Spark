import csv
import sys
import re
import matplotlib.pyplot as plt
from abc import abstractmethod

class CSVParser(object):
    @classmethod
    def loadCSVFile(cls, filePath):
        return csv.reader(open(filePath, 'r'), delimiter = ',')

class CoordinatesForCovid19Analytics(object):
    def __init__(self, filePath):
        self.rawData = CSVParser.loadCSVFile(filePath)

    def generateCoordinatesForTopNCountries(self, N):
        idx = 0
        self.countryList = list()
        self.deathPerCountry = list()
        self.positiveCasesPerCountry = list()

        next(self.rawData)

        for row in self.rawData:
            if idx <= N:
                self.countryList.append(row[1])
                self.deathPerCountry.append(int(row[2]))
                self.positiveCasesPerCountry.append(int(row[3]))
                idx += 1

class Dashboard(object):
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def display(self):
        fig, axs = plt.subplots(2, 1 , figsize = (5, 10))
        axs[0].bar(self.coordinates.countryList, self.coordinates.deathPerCountry)
        self.textValueOnChart(axs[0], self.coordinates.deathPerCountry)
        axs[0].set_xlabel('Country')
        axs[0].set_ylabel('Deaths')

        axs[1].bar(self.coordinates.countryList, self.coordinates.positiveCasesPerCountry)
        self.textValueOnChart(axs[1], self.coordinates.positiveCasesPerCountry)
        axs[1].set_xlabel('Country')
        axs[1].set_ylabel('Positive Cases')
        fig.suptitle('Covid 19 Statistics For Top ' + sys.argv[1] + ' countries at ' + sys.argv[2])

        plt.show()

    @classmethod
    def textValueOnChart(self, axs, values):
        for idx, value in enumerate(values):
            axs.text(idx, value, value, color = 'red', horizontalalignment = 'center'
                            , verticalalignment = 'baseline')

def checkCmdArgs():
    if len(sys.argv) != 3:
        raise Exception(' Please call this script with additional arguments num of countries to show and date In YYYY-MM-DD format')

    if not isDateWellFormated(sys.argv[2]):
        raise Exception(' Please call this script with additional arguments num of countries to show   date In YYYY-MM-DD format')

def isDateWellFormated(date):
    splitedDate = date.split('-')

    if len(splitedDate) != 3:
        return False

    if len(splitedDate[0]) == 4 and containsNoCharacterExceptNumber(splitedDate[0]):
        return False

    if len(splitedDate[1]) == 2 and containsNoCharacterExceptNumber(splitedDate[1]):
        return False

    if len(splitedDate[2]) == 2 and containsNoCharacterExceptNumber(splitedDate[2]):
        return False

    return True

def containsNoCharacterExceptNumber(str):
    return (re.search('[^0-9]', str) != None)

if __name__ == '__main__':
    checkCmdArgs()

    coordinates = CoordinatesForCovid19Analytics('./results/Analytics_' + sys.argv[2] + '.csv')
    coordinates.generateCoordinatesForTopNCountries(int(sys.argv[1]))

    dashboard = Dashboard(coordinates)
    dashboard.display()
