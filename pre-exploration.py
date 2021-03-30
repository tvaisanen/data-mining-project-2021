# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

        
DATA = pd.read_csv('two_years_merged_and_reduced.csv', index_col='time', parse_dates=['time'])

DATA.index = pd.to_datetime(DATA.index)

ts = pd.date_range("2000-01-01","2000-01-07")

x = DATA[(DATA.cluster == 0) & (DATA.region == 'SE3') & (DATA.index < "2000-12-31")]

LABELS = 5
x['labels'] = pd.cut(x['power-production'], labels=np.arange(LABELS), bins=LABELS)

power_min = DATA['power-production'].min()
power_max = DATA['power-production'].max()


x['Temperature'].plot()

a_week = x.iloc[1:168]


cols = ['Wind_U','Wind_V', 'WindGustSpeed',]


# df['time'] = pd.to_datetime(df['Date']) - pd.to_timedelta(7, unit='d')
# df = df.groupby(['Name', pd.Grouper(key='Date', freq='W-MON')])['Quantity']
#       .sum()
#        .reset_index()
#        .sort_values('Date')

dates =  pd.date_range("2000-01-01","2000-12-31",freq='W-MON', tz='UTC')

week_range = list(zip(dates,dates[1:-1]))


D = x[cols]


pca_model = PCA(n_components=3)

def week_pca(df, week):
    data   = df[(week[0] <= df.index) & (df.index < week[1])]
    if not data.empty and data.shape[0] == 168:
        decomp = pca_model.fit_transform(data)
        return pd.DataFrame(decomp, index=data.index)

weeks_after_pca = pd.concat([
    week_pca(D, week)
    for week 
    in week_range
])


def vectorize_week(df, week):
    data   = df[(week[0] <= df.index) & (df.index < week[1])]
    if not data.empty and data.shape[0] == 168:
        return pd.DataFrame(
            data.to_numpy().reshape(7,72), 
            index=data.resample('1D').sum().index)

weeks_vectorized = pd.concat([
    vectorize_week(weeks_after_pca, week)
    for week 
    in week_range
])

labels = pd.cut(
       x['power-production'].resample('1D').mean(),
       labels=np.arange(LABELS), bins=LABELS)

weeks_vectorized['label'] = labels

train = weeks_vectorized.iloc[0:240]
test = weeks_vectorized.iloc[240:]

X = train[np.arange(72)]
y = train['label']

T = test[np.arange(72)]
z = test['label']

from sklearn.svm import SVC
from sklearn import metrics


clf = SVC(gamma='auto')
clf.fit(X,y)

y_pred = clf.predict(T)
test['pred'] = y_pred


from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(random_state=0).fit(X, y)
y_pred_2 = clf.predict(T)


print(clf.score(T, y_pred_2))

# metrics.accuracy_score(y_pred, T)

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB().fit(X,y)
y_pred_3 = gnb.predict(T)

from sklearn.neighbors import KNeighborsClassifier

knb = KNeighborsClassifier(3).fit(X,y)
y_pred_4 = knb.predict(T)


x = np.arange(0,len(y_pred))
plt.figure()

plt.plot(x, y_pred)
#plt.plot(x, y_pred_2)
#plt.plot(x, y_pred_3)
plt.plot(x, y_pred_4)

print(metrics.accuracy_score(test.label, y_pred))
print(metrics.accuracy_score(test.label, y_pred_2))
print(metrics.accuracy_score(test.label, y_pred_3))
print(metrics.accuracy_score(test.label, y_pred_4))




