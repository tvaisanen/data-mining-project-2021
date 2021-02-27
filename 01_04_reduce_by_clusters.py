#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 11:06:12 2021

@author: tvaisanen
"""

import constants as c
import pandas as pd
import xarray as xr
import os 

weather_stations = pd.read_csv(
    './weather_stations_clustered.csv').drop(
        columns=['Unnamed: 0', "ensemble_member"])


weather_stations_lat_lon = weather_stations.set_index(
    ['lat','lon']).drop(
                    columns=['time','x','y', 'weight'])
        


for fn in os.listdir(c.WEATHER_DATA_PATH):
    try:
        ds = xr.open_dataset(os.path.join(c.WEATHER_DATA_PATH,fn))
        df = ds.to_dataframe().rename(
            columns={
            'latitude':c.LAT,
            'longitude':c.LON
        })
        
        df.reset_index(inplace=True)
        
        joined_data = df.set_index([c.LAT, c.LON]).join(
            weather_stations_lat_lon, 
                          how='left', 
                          lsuffix='_left', 
                          rsuffix='_right').dropna()
                    
        reduced = joined_data.groupby(['time', 'cluster', 'region']).mean()
        reduced.reset_index(inplace=True)
        reduced = reduced.set_index('time')
        reduced.index = pd.to_datetime(reduced.index)
        
        reduced.to_csv('./reduced-data/{}.csv'.format(fn.split(".")[0]))
    except Exception as e:
        print(e)
        print('data reduction failed with file: {}'.format(fn))
     

"""

Reasoning behind the process


df_weather_data =  xr.open_dataset(
    os.path.join(c.WEATHER_DATA_PATH, 'task0_0226.nc')
    ).to_dataframe().rename(
        columns={
            'latitude':c.LAT,
            'longitude':c.LON
    })

h = h.set_index(['lat','lon']).drop(columns=['x','y','ensemble_member'])
w = weather_stations.set_index(['lat','lon']).drop(columns=['time','x','y','weight'])


hw = h.join(w, 
       how='left', 
       lsuffix='_left', 
       rsuffix='_right').dropna()


hw.to_csv('test_merge.csv')

test = hw[(hw.cluster == 0) & (hw.region == 'SE1')].groupby('time').mean()
test['region'] = 'SE1'
test.to_csv('2002_02_26_region_SE1_cluster0.csv')

f = plt.figure(figsize=(15,15))
f.add_subplot(111)
plt.plot(test.index, test.Temperature - 273.15)
f.add_subplot(211)
plt.plot(test.index, test.RelativeHumidity)
plt.show()
"""



