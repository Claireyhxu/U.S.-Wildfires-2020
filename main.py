#Python Project
#Claire, Rishabh, Jingbo, Yewei

from dataExtraction import DataExtraction
from rawData import RawData
from analysis import Analysis
import pandas as pd


def displayMenu():
    ## Displays initial menu for the user
    ## Takes choice input
    
    print()
    print('Chose from below options:')
    print('1. Overview Analysis')
    print('2. State Level Analysis')
    print('3. Month Wise Analysis')
    print('4. Get Raw Data')
    print('5. Quit')
    
    choice = int(input('Enter choice: '))
    
    if choice < 1 or choice > 5:
        choice = 5
    
    return choice


def overview(events_dataframe):
    #Function for choice 1
    #Overview of the analysis
    obj1 = Analysis(events_dataframe)
    obj1.summary(events_dataframe)
    obj1.byMonth()
    obj1.byTime()
    obj1.byLocation()
    obj1.frqGraph()

    
def stateLevel(events_dataframe):
    #Function for choice 2
    #State level analysis of the data
    obj1 = Analysis(events_dataframe)
    obj1.State()
  
    
def monthWise(events_dataframe):
    #Function for choice 3
    #Month wise analysis of the data
    obj1 = Analysis(events_dataframe)
    obj1.Month()

    
def rawData(events_dataframe):
    #Function for choice 4
    #Get NASA API raw data based on county / city name
    obj1 = RawData(events_dataframe)
    obj1.printRawData()


def main():
    #Main method
    
    #Get the data from the NASA API and store it in a dataframe
    nasa_api = DataExtraction()
    eventsDf = pd.DataFrame()
    eventsDf = nasa_api.API()
    
    #Display choice
    choice = displayMenu()
    
    #Loop on choice until 'Quit' option
    while choice != 5:
        
        if choice == 1:
            overview(eventsDf)
        elif choice == 2:
            stateLevel(eventsDf)
        elif choice == 3:
            monthWise(eventsDf)
        elif choice == 4:
            rawData(eventsDf)
    
        choice = displayMenu()


if __name__ == '__main__':
    main()