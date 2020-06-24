import csv
import matplotlib.pyplot as plt

class csvParser(object):
    @classmethod
    def loadCSV(cls, filePath):
        return csv.reader(open(filePath, 'r'), delimiter = ',')

    @classmethod
    def generateCoordinatesForNCountries(cls, plots, N):
        idx = 0
        countryList = list()
        deathPerCountry = list()
        positiveCasesPerCountry = list()

        next(plots)

        for row in plots:
            if idx <= N:
                countryList.append(row[1])
                deathPerCountry.append(int(row[2]))
                positiveCasesPerCountry.append(int(row[3]))
                idx += 1

        return [countryList, deathPerCountry, positiveCasesPerCountry]


class resultDisplay(object):
    def __init__(self, csvParser):
        self.csvParser = csvParser

    def prepareCoordinates(self):
        self.coordinates = self.csvParser.generateCoordinatesForNCountries(self.csvParser.loadCSV('/home/size7311/Covid19-Analytics-With-Spark/Analytics_06-23-2020.csv'), 5)

    def display(self):
        self. prepareCoordinates()

        fig, axs = plt.subplots(2, 1 , figsize = (5, 10))
        axs[0].bar(self.coordinates[0], self.coordinates[1])
        axs[0].set_xlabel('Country')
        axs[0].set_ylabel('Deaths')

        axs[1].bar(self.coordinates[0], self.coordinates[2])
        axs[1].set_xlabel('Country')
        axs[1].set_ylabel('Positive Cases')
        fig.suptitle('Covid 19 Statistics')

        plt.show()

if __name__ == '__main__':
    displayer = resultDisplay(csvParser())
    displayer.display()
