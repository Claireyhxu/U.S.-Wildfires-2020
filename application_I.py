#analysis.py
#Class for data analysis

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objs as go
import plotly
from plotly.offline import download_plotlyjs
from plotly.offline import iplot


#Analysis class
class Analysis:
    
    def __init__(self, events_df):
        #Constructor
        #Cleaning and pre-processing the data
        
        self.__event = events_df.copy()
        
        # We only needs data from the United States
        self.__event = self.__event[self.__event['country']=='United States']
        
        # Only focus on Wildfires
        self.__event = self.__event[self.__event['categories title']=='Wildfires']
        
        # Remove the index in the original dataset and get a new index
        self.__event = self.__event.reset_index(drop = True)
        
        # Drop rows with NA
        self.__event = self.__event.dropna()
        
        # Eventdate column includes year, month, day, and time.
        #We want to separate them into several columns
        eventdate = self.__event['eventdate']
        self.__event['date'] = eventdate.apply(lambda  x:x.split('T')[0])
        self.__event['time'] = eventdate.apply(lambda  x:x.split('T')[1])
        date = self.__event['date']
        self.__event['year'] = date.apply(lambda  x:x.split('-')[0])
        self.__event['month'] = date.apply(lambda  x:x.split('-')[1])
        self.__event['day'] = date.apply(lambda  x:x.split('-')[2])
        time = self.__event['time']
        self.__event['hour'] = time.apply(lambda  x:x.split(':')[0])
        
        self.__event['longitude'] = ''
        self.__event['latitude'] = ''
        
        coordinates_idx = self.__event.columns.get_loc('coordinates')
        lng_idx = self.__event.columns.get_loc('longitude')
        lat_idx = self.__event.columns.get_loc('latitude')
        
        for i in range(len(self.__event.index)):
            self.__event.iloc[i,lng_idx] = self.__event.iloc[i,coordinates_idx][0]
            self.__event.iloc[i,lat_idx] = self.__event.iloc[i,coordinates_idx][1]
        
    
    def convertMonth(self, month):
        #Convert the month number to month name
        if month == 8:
            return 'August'
        elif month == 9:
            return 'September'
        elif month == 10:
            return 'October'
        elif month == 11:
            return 'November'
        elif month == 12:
            return 'December'

    
    def summary(self, events_df):    
        #Print the inital summary such as size of data frame, number of rows,
        #number of columns
        #For choice 1 of the user
        
        rawdata = events_df.copy()
        
        print()
        print(f"size of the raw dataset: {rawdata.shape}")
        print()
        print('The dataset consists of {:d} natural events over the \
course of 2013 to 2019. There are {:d} attributes (or columns) \
associated with each natural event.'.format(rawdata.shape[0], rawdata.shape[1]))
        print()
        print(rawdata.head(n=5))
        
        # we can see that our data only focus on 2020
        years = self.__event['year'].unique()
        print()
        print(f'Number of unique years in dataset: {years}')
        months = self.__event['month'].unique()
        print(f'Number of unique months in dataset: {months}')
        self.__event = self.__event.sort_values(by = 'month')


    def byMonth(self):
        #Month data within the Overview summary
        #For choice 1 of the user
        
        count_aug = 0
        count_sep = 0
        count_oct = 0
        count_nov = 0
        count_dec = 0
        
        #Counting the number of wildfires per month
        for i in range(len(self.__event.index)):
            if self.__event.iloc[i]['month'] == '08':
                count_aug = count_aug + 1
            elif self.__event.iloc[i]['month'] == '09':
                count_sep = count_sep + 1
            elif self.__event.iloc[i]['month'] == '10':
                count_oct = count_oct + 1
            elif self.__event.iloc[i]['month'] == '11':
                count_nov = count_nov + 1
            elif self.__event.iloc[i]['month'] == '12':
                count_dec = count_dec + 1
        
        #Printing the number of wildfires per month
        print()
        print("The number of wildfires that happened in August is:", count_aug)
        print("The number of wildfires that happened in September is:", count_sep)
        print("The number of wildfires that happened in October is:", count_oct)
        print("The number of wildfires that happened in November is:", count_nov)
        print("The number of wildfires that happened in December is:", count_dec)
        
        
        #Plotting the month summary
        count = pd.DataFrame({'Month':['Aug','Sep','Oct','Nov','Dec'],
                              'Count':[count_aug, count_sep, count_oct,count_nov,count_dec]})
        x = count['Month']
        y = count['Count']
        plt.figure(figsize=(15,10))
        plt.title('Number of wildfires by month')
        plt.xlabel('Month')
        plt.ylabel('Number of wildfires')
        plt.bar(x,y, color = 'firebrick')
        plt.show()


    def byTime(self):
        #Time data within the Overview Summary
        #For choice 1 of the user
        
        # Ee divide a day to daytime and nighttime
        # daytime begin from 7AM to 5PM based on https://www.worlddata.info/america/usa/sunset.php
        # and nighttime begin from 5PM to 7AM in the next day
        
        count_daytime = 0
        count_nighttime = 0
        
        #Counting the number of wildfires as per time (daytime/nighttime)
        for i in range(len(self.__event.index)):
            hour = int(self.__event.iloc[i]['time'][0])*10 + int(self.__event.iloc[i]['time'][1])
            if 7 < hour <17:
                count_daytime = count_daytime + 1
            else:
                count_nighttime = count_nighttime + 1
        
        #Printing the number of wildfires as per time
        print()
        print("The number of wildfires that happened in daytime is:", count_daytime)
        print("The number of wildfires that happened in nighttime is:", count_nighttime)
        
        #Plotting the time based wildfire summary
        count = pd.DataFrame({'Time':['Daytime','Nighttime'],
                              'Count':[count_daytime, count_nighttime]})
        x = count['Time']
        y = count['Count']
        plt.figure(figsize=(15,10))
        plt.title('Number of wildfires by time')
        plt.xlabel('Time')
        plt.ylabel('Number of wildfires')
        plt.bar(x,y, color = 'firebrick')
        plt.show()
        # Based on the result, we can conclude that wildfires are more likely to happen in daytime, compared to nighttime.         
        
        
    def byLocation(self):
        #Location data within the Overview Summary
        #For choice 1 of the user
        
        #Plotting location wise wildfire summary data
        state_idx = self.__event['state'].value_counts().index
        state_v = self.__event['state'].value_counts().values
        plt.figure(figsize=(10,15))
        sns.set_context('talk')
        sns.barplot( x = state_v, y = state_idx, palette  = 'Spectral');
        plt.title('Number of wildfire incidents based on NASA\'s API')
        plt.xlabel('Number of wildfire incidents in 2020, AUG - DEC')
        plt.show()


    def frqGraph(self):
        #For choice 1 of the user
        #Plot the coordinates of wildfires on the US map
        
        event = self.__event.copy()
        
        event['month'] = [i[5:7] for i in event['eventdate']]
        event['month'] = event['month'].astype(int)
        event['month_char'] = event['month'].apply(self.convertMonth)
        
        #Setting the layout of the output
        #Title, image size, legend details
        layout = dict(
            title = 'US Wildfires Aug - Dec 2020',
            autosize = False,
            width = 1000,
            height = 1200,
            hovermode = False,
            legend = dict(
                x = 0.7,
                y = -0.1,
                bgcolor = "rgba(255, 255, 255, 0)",
                font = dict(size = 11),
                )
            )        
        
        months = ['August', 'September', 'October', 'November', 'December']
        mapdata = []
        
        #Plotting the points on the US map
        #Each wildfire has a coordinate which is plotted on the map
        for i in range(len(months)):
            geo_key = 'geo' + str(i+1) if i != 0 else 'geo'
            lons = list(event[event['month_char'] == months[i]]['longitude'])
            lats = list(event[event['month_char'] == months[i]]['latitude'])
        
            mapdata.append(
                dict(
                    type = 'scattergeo',
                    showlegend = False,
                    lon = lons,
                    lat = lats,
                    geo = geo_key,
                    name = str(months[i]),
                    marker = dict(
                        color = 'rgb(255, 0, 0)',
                        opacity = 0.5)))
            
            mapdata.append(
                dict(
                    type = 'scattergeo',
                    showlegend = False,
                    lon = [-78],
                    lat = [47],
                    geo = geo_key,
                    text = [months[i]],
                    mode = 'text',))
            
            layout[geo_key] = dict(
                scope = 'usa',
                showland = True,
                landcolor = 'rgb(229, 229, 229)',
                showcountries = False,
                domain = dict(x = [], y = []),
                subunitcolor = 'rgb(255, 255, 255)',)
            
        z = 0
        COLS = 2
        ROWS = 3
        
        for y in reversed(range(ROWS)):
            for x in range(COLS):
                geo_key = 'geo' + str(z+1) if z != 0 else 'geo'
                layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
                layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
                z = z + 1
                if z == 5:
                    break
        
        
        fig = dict(data = mapdata, layout = layout)
        config = {'scrollZoom': False}
        iplot(fig, filename = 'US Wildfires 2020 Summer', config = config)



    def day_night(self, time):
        if time > 7 & time < 17:
            return 'Day'
        else:
            return 'Night'


    def State(self):
        #State Level Analysis
        #For choice 2 of the user
        
        event = self.__event.copy()
        
        #User input for State name
        statename = input('Enter a state name: ')
        print()
        
        #Filter data using state name and creating a dataframe of filtered data
        event['month'] = event['month'].astype(int)
        event['month_char'] = event['month'].apply(self.convertMonth)
        state_month_df = event.groupby(['state', 'month_char'])['state'].count().reset_index(name = "count")
        
        state_month = state_month_df.loc[state_month_df['state'] == statename]
        if state_month.empty:
            print('No wildfires in this state!')
            return
        
        #Print state name and wildfire count per month
        print('The state ' + statename + ' had wildfires in the following month(s) with count(s): ')
        print()
        print(state_month)
        print('-'*40)
        
        #State day-night count
        print()
        event['hour'] = [i[0:2] for i in event['time']]
        event['hour'] = [int(i[0])*10 + int(i[1]) for i in event['hour']]
            
        event['day_night'] = event['hour'].apply(self.day_night)
        state_daynight_df = event.groupby(['state', 'day_night'])['state'].count().reset_index(name = "count")
        
        print('The state ' + statename + ' had wildfires by day and night: ')
        state_daynight = state_daynight_df.loc[state_daynight_df['state'] == statename]
        print()
        print(state_daynight)
        print('-'*40)
        
        #County wise summary within the state
        print()
        print('Counties of state', statename, 'where wildfire happened in past 5 months: \n')
        statedata = event[event['state']==statename][['state','city','date','time']].sort_values(by = 'date')
        print(statedata)
        print('-'*70)
        
        print()
        print('Frequency of wildfires by each county in state', statename, ':')
        countydata = statedata['city'].value_counts()
        print(countydata)
        
        #State ranking
        print()
        state_rank = event['state'].value_counts().rank(method="min")[statename]
        state_freq = event['state'].value_counts()[statename]
        print('Total frequency of wildfires in', statename, 'is', state_freq)
        print()
        print(statename, 'ranks', state_rank, 'in all', len(event['state'].value_counts()), 'states.')
        print('\nP.S: Ranking range is from 1 to 12: 1 means the state has least frequency of wildfires, and 12 means the highest frequency.')
    

    
    def Month(self):
        #Month level analysis
        #For choice 3 of the user
        
        event = self.__event.copy()
        
        #Dict for converting month name to number
        month_number = {'August':8,'September':9,
                'October':10,'November':11, 'December':12}

        #User input for month name
        user_month = input("Enter a month from August to December: ")
        if user_month in month_number.keys():
            monthinnumber = month_number[user_month]
        else:
            print('Invalid month! Enter from the given range only.')
            return
        
        #Filter data based on month the user entered
        event['month'] = event['month'].astype(int)
        event['month_char'] = event['month'].apply(self.convertMonth)
        event_inmonth = event[event['month'] == monthinnumber]
        
        if event_inmonth.empty:
            print('No wildfires in this month!')
            return
        
        #Wildfire count in the given month
        event_inmonth = event_inmonth.reset_index(drop = True)
        print("The number of wildfires that happened in", user_month,"is: ", max(event_inmonth.index)+1)
        
        #Plot of state wise count for the given month
        state_idx = event_inmonth['state'].value_counts().index
        state_v = event_inmonth['state'].value_counts().values
        plt.figure(figsize=(10,15))
        plt.title('Number of wildfires by state in the month')
        plt.xlabel('Number of wildfires')
        sns.set_context('talk')
        sns.barplot(x = state_v, y = state_idx, palette  = 'Spectral')
        plt.show()
        
        #Daytime-Nighttime count for the given month
        count_daytime = 0
        count_nighttime = 0
        for i in range(max(event_inmonth.index)+1):
            hour = int(event_inmonth.iloc[i]['time'][0])*10 + int(event_inmonth.iloc[i]['time'][1])
            if 7 < hour <17:
                count_daytime = count_daytime + 1
            else:
                count_nighttime = count_nighttime + 1
        
        daynight = pd.DataFrame({'Time':['Daytime','Nighttime'],
                              'Count':[count_daytime, count_nighttime]})
        print()
        print("Number of wildfires by time in the month:")
        print()
        print(daynight)