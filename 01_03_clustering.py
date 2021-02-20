#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 18:14:31 2021

@author: tvaisanen
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas
import constants as c
from sklearn.cluster import KMeans
from collections import Counter


def plotting(weather_coordinates, pr_coordinates, cluster_centers):

    world = geopandas.read_file(c.MAP)
    swe = world[world['admin'] == 'Sweden']  # Filter out Sweden from the world
    base = swe.plot(color='white', edgecolor='black',  figsize=(15,15))

    plt.scatter(cluster_centers[:,1], cluster_centers[:,0], s=400, c="white", edgecolors="black", alpha=0.5)
    plt.plot(weather_coordinates.lon, weather_coordinates.lat,"ro", markersize=1, alpha=0.5)
    plt.plot(pr_coordinates.lon, pr_coordinates.lat, 'bo', markersize=1, alpha=0.5)


def k_means_clustering(df, pr_coordinates, config):
    
    kmeans = KMeans(
             init="random",
             n_clusters=config["n_clusters"],
             n_init=10,
             max_iter=300,
             random_state=42
        )
    
    kmeans.fit(pr_coordinates)
    
    prediction = kmeans.predict(df[[c.LAT, c.LON]])

    
    def calc_distance(row):
        return np.linalg.norm(
            [row.lat,row.lon] - kmeans.cluster_centers_[row.cluster].T
        )
        
    
    df['cluster'] = prediction   
    df['distance'] = df.apply(calc_distance, axis=1)
    
    distance = config["cluster_size"]

    return(df[df.distance <= distance], kmeans.labels_, kmeans.cluster_centers_)



windturbines = pd.read_csv("turbines.csv")

df = pd.read_csv('weather_stations_all.csv')

cluster_coordinates_by_region = [ 
    windturbines[[c.LAT,c.LON]][windturbines.region == region] 
    for region 
    in c.PRICE_REGIONS
]


config = {
   'n_clusters': 10,
   'cluster_size': 0.4,
}

selected_weather_stations = list()

for i, cluster in enumerate(cluster_coordinates_by_region):
    
    # Get clusters for each region
    weather_coordinates, labels, cluster_centers = k_means_clustering(df, cluster, config) 
    
    f = plt.figure(figsize=(15,10))
    
    plotting(weather_coordinates, cluster, cluster_centers)
    
    plt.savefig(
        os.path.join(
            c.FIGURES_PATH,
            '01_03_weather_station_clusters_{}.png'.format(c.PRICE_REGIONS[i])
            )       
        )
    
    selected_weather_stations.append(weather_coordinates)




