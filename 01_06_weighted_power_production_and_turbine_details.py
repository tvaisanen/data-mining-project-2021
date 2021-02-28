# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
        
X = pd.read_csv('two_years_merged_and_reduced.csv', index_col='time', parse_dates=['time'])    

        

def wind_angle(row):
    x = row['Wind_U']
    y = row['Wind_V']
    
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 and y > 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    else:
        return 4



january = X[np.logical_and.reduce([
    X.index >= "2000-01-01",
    X.index <  "2000-02-01"])]

january['quadrant'] = january.apply(wind_angle, axis=1)

se1 = january[january['region'] == 'SE1']
se2 = january[january['region'] == 'SE2']
se3 = january[january['region'] == 'SE3']
se4 = january[january['region'] == 'SE4']



def normalize(df, cols):
    return pd.DataFrame(
        StandardScaler().fit_transform(df[cols].resample('1H')),
        index=df.index,
        columns=cols)


for price_region in [se1,se2,se3,se4]:
    df_tmp = normalize(price_region, ['WindGustSpeed','power-production'])
    df_tmp.plot()

        