# -*- coding: utf-8 -*-

import geopandas
import pandas as pd
import matplotlib.pyplot as plt

import constants as c

df_weather_stations = pd.read_csv('./weather_stations.csv').astype(float)
df_weather_stations[[c.LAT, c.LON]] = df_weather_stations[[c.LAT,c.LON]].astype(float)
world = geopandas.read_file("../geokoodi/ne_10m_admin_1_states_provinces.shp")
swe = world[world['admin'] == 'Sweden']  # Filter out Sweden from the world
base = swe.plot(color='white', edgecolor='black', figsize=(15,15))

df_weather_stations[df_weather_stations == 'SE1']

plt.plot(
   df_weather_stations[df_weather_stations == 'SE1'][c.LON],
   df_weather_stations[df_weather_stations == 'SE1'][c.LAT],
    "ro", 
    markersize=1, 
    alpha=0.1
)

# plt.plot(temp[1]['longitude'],temp[1]['latitude'],"bo", markersize=1, alpha=0.1)
# plt.plot(temp[2]['longitude'],temp[2]['latitude'],"go", marker  size=1, alpha=0.1)
# plt.plot(temp[3]['longitude'],temp[3]['latitude'],"yo", markersize=1, alpha=0.1)