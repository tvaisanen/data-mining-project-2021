# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import xarray as xr
import os

WEATHER_DATA_PATH = '../data'
PRICE_REGIONS = ['SE1','SE2','SE3','SE4']
LAT = 'lat'
LON = 'lon'
REGION = 'region'
TIME = 'time'

# Load data

# Data frame of: time, SE1, SE2, SE3, SE4
df_windpower = pd.read_csv('../windpower.csv').rename(columns={'Unnamed: 0':TIME})

# Data frame of: region, lat, long
df_turbines = pd.read_csv('../windturbines.csv')[
    ['Price region', 'Latitude', 'Longitude']
    ].rename(columns={
        'Price region':REGION, 
        'Latitude':LAT, 
        'Longitude':LON})

# Extract distinct weather stations from the first weather data file
df_weather_stations =  xr.open_dataset(
    os.path.join(WEATHER_DATA_PATH, 'task0_0226.nc')
    ).to_dataframe()[['latitude','longitude']].rename(
        columns={
            'latitude':LAT,
            'longitude':LON}
        ).drop_duplicates()
        
df_weather_stations.to_csv('weather_stations_all.csv')
        
# Get min max lat long boxes
wt_min = df_turbines.groupby(REGION).min()
wt_max = df_turbines.groupby(REGION).max()

arr_df_weather_stations = [
    df_weather_stations[
         (wt_min.loc[se].lat < df_weather_stations.lat) & 
         (wt_max.loc[se].lat > df_weather_stations.lat) &
         (wt_min.loc[se].lon < df_weather_stations.lon) & 
         (wt_max.loc[se].lon > df_weather_stations.lon)]  
    for se in PRICE_REGIONS
]

# label regions based on the box
for i, region in enumerate(PRICE_REGIONS):
    arr_df_weather_stations[i][REGION] = region
    

df_weather_stations = pd.concat(arr_df_weather_stations)

df_turbines.to_csv('./turbines.csv')
df_weather_stations.to_csv('./weather_stations.csv',columns=[REGION,LAT,LON])
df_windpower.to_csv('./power_production.csv')