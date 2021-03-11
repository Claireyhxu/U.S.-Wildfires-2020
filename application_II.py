#rawData.py
#Class for webscrapping and printing raw data

import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
from zipfile import ZipFile as zipf
from io import BytesIO


#RawData Class
class RawData:
    
    def __init__(self, events_df):
        #Contructor
        
        #Initialise the variables
        self.__choice = 0
        self.__choice_name = ''
        self.__events_df = events_df.copy()
        
        #Present the user with choices and take input
        print('')
        print('''This choice is for getting the raw data of NASA API. \
              The API data is grouped by county names, but the user has the \
                  option to enter city name or county name.\n''')
        print('Options:')
        print('1. Search by county name')
        print('2. Search by city name')
        
        #Get choice number and city/county name
        self.__choice = int(input('Enter the choice: '))
        self.__choice_name = str(input('Enter the name (in camel case): '))
    
    
    def webScrapping(self):
        #Method for web scrapping
        
        #Wesite URL
        website = 'https://simplemaps.com'
        url = 'https://simplemaps.com/resources/free-country-cities'
        
        ### Extracting 'US Cities' CSV Link ###
        
        #Accessing the webpage
        page = requests.get(url)
        page.raise_for_status()
        page_data = bs(page.content, 'html.parser')
        
        #Finding the CSV link and store it in variable 'csv_url'
        header_tags = page_data.find('ul', class_='nav nav-pills')
        header_ahref_list = header_tags.select('a')
        
        for row in header_ahref_list:
            if row.get_text().strip() == 'US Cities':
                temp_link = row['href']
                csv_url = website+temp_link
                break
        
        ### Extracting City Data ###
        
        #Accesing the webpage
        city_page = requests.get(csv_url)
        city_page.raise_for_status()
        city_page_data = bs(city_page.content, 'html.parser')
        
        #Creating cities dataframe
        csv_tags = city_page_data.find('div', class_='modal-footer')
        csv_ahref_list = csv_tags.select('a')
        
        for row in csv_ahref_list:
            if row.get_text().strip() == 'Yes, proceed with download':
                temp_link = row['href']
                download_url = website+temp_link
                break
        
        #Handling Zip File
        csv_request = requests.get(download_url)
        csv_request.raise_for_status()
        zip_file = zipf(BytesIO(csv_request.content))
        
        city_df = pd.read_csv(zip_file.open('uscities.csv'))  
        
        return city_df
    
    
    def printRawData(self):     
        #Method for printing the raw data from NASA API
        
        #Choice 1
        #Print data using county name
        if self.__choice == 1:
            if self.__choice_name[-1:-7] != ' County':
                self.__choice_name += ' County'
            
            county_data = self.__events_df[self.__events_df.city == self.__choice_name]
            
            if county_data.empty:
                print('No data found for the selected county!')
            else:
                county_data.reset_index(inplace=True)
                print()
                print('The number of wilfires in this county are: ', len(county_data.index))
                print(county_data[['eventdate', 'coordinates', 'state', 'city']])
            
        #Choice 2
        #Print data using city name
        elif self.__choice == 2:
            city_df = pd.DataFrame()
            
            #Extracting county name from city name
            #using the webScrapping method
            city_df = self.webScrapping()  
            
            city_data= city_df[city_df.city == self.__choice_name]
            if city_data.empty:
                print('City not in csv database!')
                return
            
            county_name = city_data.iloc[0,5]
            county_name += ' County'
            
            county_data = self.__events_df[self.__events_df.city == county_name]
            
            if county_data.empty:
                print('No data found for the selected city!')
            else:
                county_data.reset_index(inplace = True)
                print()
                print('The number of wilfires in this county are: ', len(county_data.index))
                print(county_data[['eventdate', 'coordinates', 'state', 'city']])
                
        else:
            print('Wrong choice! Run again!')
        