# -*- coding: utf-8 -*-

import pandas as pd

data = pd.read_csv('2002_02_26_test_merge.csv')


reduced_data = data.groupby(['time', 'cluster', 'region']).mean()