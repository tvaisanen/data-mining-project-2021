# -*- coding: utf-8 -*-

import geopandas
import pandas as pd
import matplotlib.pyplot as plt

import constants as c

df_weather_stations_all = pd.read_csv('./weather_stations_all.csv')
df_weather_stations = pd.read_csv('./weather_stations.csv')

df_weather_stations[[c.LAT, c.LON]] = df_weather_stations[[c.LAT,c.LON]].astype(float)
world = geopandas.read_file(c.MAP)
swe = world[world['admin'] == 'Sweden']  # Filter out Sweden from the world

f = plt.figure()

swe.plot(color='white', edgecolor='black', figsize=(15,15))
plt.plot(
   df_weather_stations_all.lon,
   df_weather_stations_all.lat,
    "ro", 
    markersize=1, 
    alpha=0.5
)

plt.savefig('figures/01_02_all_weather_stations.png')

f = plt.figure()

swe.plot(color='white', edgecolor='black', figsize=(15,15))
plt.plot(
   df_weather_stations.lon,
   df_weather_stations.lat,
    "ro", 
    markersize=1, 
    alpha=0.5
)

plt.savefig('figures/01_02_boxed.png')

COLORS = ['ro','bo','ro','yo']

for i, region in enumerate(c.PRICE_REGIONS):   
    f = plt.figure()
    swe.plot(color='white', edgecolor='black', figsize=(15,15))
    plt.plot(
        df_weather_stations[df_weather_stations.region == region].lon,
        df_weather_stations[df_weather_stations.region == region].lat,
        COLORS[i], 
        markersize=1, 
        alpha=1)
    plt.savefig('figures/01_02_boxed_{}.png'.format(region))
