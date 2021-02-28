#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 11:06:43 2021

"""

## JOIN THE POWER PRODUCTION DATA

import os
import constants as c
import pandas as pd
from datetime import datetime

df_power_production = pd.read_csv('power_production.csv', index_col='time').drop(columns=['Unnamed: 0'])

df_power_production.index = pd.to_datetime(df_power_production.index, utc=True)

def pick_power_production(row):
    try:
        return row[row.region]
    except Exception as e:
        print(e)
        print('pick_power_production failed for row')
        print(row[row])

def run():
    for filename in os.listdir(c.REDUCED_DATA_PATH):
        try:
            df_weather = pd.read_csv(os.path.join(c.REDUCED_DATA_PATH, filename), index_col='time', parse_dates=['time'])
            df_weather.index = pd.to_datetime(df_weather.index, utc=True)
    
            df_weather_n_power = df_weather.merge(df_power_production, on='time')
        
            df_weather_n_power['power-production'] = df_weather_n_power.apply(pick_power_production, axis=1)
            df_weather_n_power = df_weather_n_power.drop(columns=c.PRICE_REGIONS, axis=1)

            df_weather_n_power.drop(
                columns=['ensemble_member','x','y']
                ).to_csv(
                    './reduced-weather-with-power-consumption/{}.csv'.format(
                        str(df_weather_n_power.index[0].date())))


        except Exception as e:
            print(e)
            print('data reduction failed with file: {}'.format(filename))
         
DAILY_REDUCED_PATH = "reduced-weather-with-power-consumption"

def join_daily_files():
    
    files = os.listdir(DAILY_REDUCED_PATH)
    
    full_data = pd.read_csv(
            os.path.join(
                DAILY_REDUCED_PATH,
                files[0]), 
            index_col='time', 
            parse_dates=['time'])
    
    for filename in files[1:]:
        
        df_weather_tmp = pd.read_csv(
            os.path.join(
                DAILY_REDUCED_PATH,
                filename), 
            index_col='time', 
            parse_dates=['time'])
        
        full_data = pd.concat([full_data, df_weather_tmp], axis=0)
    
    return full_data
        
        


