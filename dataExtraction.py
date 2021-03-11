#dataExtraction.py
#Class for NASA data extraction

from geopy.geocoders import Nominatim
import json
import requests
import pandas as pd
import re


#DataExtraction class
class DataExtraction:

    def __init__(self):
        #Constructor
        self.__address = ''
        self.__event_df = pd.DataFrame()
        

    def __getAddress(self,latitude, longitude):
        #Get address using the latitude and longtiude
        #Nominatim python library used
        loc_string = str(latitude) + ', ' + str(longitude)
        geolocator = Nominatim(user_agent="Chrome/74.0.3729.169")
        
        try:
            location = geolocator.reverse(loc_string)
            self.__address = location.address
        except TypeError:
            self.__address = 'NA'
        
        return self.__address

    
    def __getCountry(self, address):
        #Get country name from the address string
        country_list = address.split(', ')
        country_list = country_list[-4:]
        if len(country_list) == 4 and re.fullmatch(r'^[0-9]+$', country_list[2]):
            del country_list[2]
        elif len(country_list) == 4:
            del country_list[0]
        return country_list


    def API(self):
        #NASA API code
        
        #Access the api and extract events
        headers = {'Content-Type': 'application/json'}
        url = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events'
        response = requests.get(url, headers = headers) 
        
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
         
        listevent = data['events']
        catid =[]
        cattitle = []
        eventdate = []
        coordinates = []
        country = []
        state = []
        city = []
        
        #Create lists for filling the final dataframe
        for i in range(len(listevent)):
            catid.append(listevent[i]['categories'][0]['id'])
            cattitle.append(listevent[i]['categories'][0]['title'])
            eventdate.append(listevent[i]['geometries'][0]['date'])
            
            if len(listevent[i]['geometries'][0]['coordinates']) == 1:
                coordinates.append(listevent[i]['geometries'][0]['coordinates'][0][0])
            else:
                coordinates.append(listevent[i]['geometries'][0]['coordinates'])
            
            temp_list = self.__getCountry(self.__getAddress(coordinates[-1][1], coordinates[-1][0]))
            
            if len(temp_list) > 2:
                country.append(temp_list[2])
                state.append(temp_list[1])
                city.append(temp_list[0])
            else:
                country.append('NA')
                state.append('NA')
                city.append('NA')
        
        #Create the final events dataframe
        #Columns: Category id, Category title, Event date,
        #Coordinates, Country, State, City 
        event = pd.DataFrame({'categories id':catid, 'categories title':cattitle,
                             'eventdate':eventdate, 'coordinates':coordinates, 'country':country,
                             'state': state, 'city': city})
        
        self.__event_df = event.copy()
        return self.__event_df