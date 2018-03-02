import pandas as pd
import numpy as np
import matplotlib
%matplotlib inline

df = pd.DataFrame()
print(df)
df['name'] = ['Bilbo', 'Frodo', 'Samwise']

df
df.assign(height = [0.5, 0.4, 0.6])
df = pd.read_csv('data/skyhook_2017-07.csv', sep=',')

df.head()

df.shape

df.columns
df['cat_name'].unique()
df['cat_name']
df.cat_name

one_fifty_eight = df[df['hour'] == 158]

df[(df['hour'] == 158) & (df['count'] > 50)].shape

one_fifty_eight.shape

bastille = df[df['date']=='2017-07-13']
bastille.head()

#Greater than average cells
lovers_of_bastille = bastille[bastille['count'] > bastille['count'].mean()]

lovers_of_bastille['count'].describe()
df.groupby('date')['count'].sum().plot()
df.groupby('date')['count'].sum().describe()
df['count'].max()
df['count'].min()

df['hour'].unique()
jul_sec = df[df['date'] == '2017-07-02']

jul_sec.groupby('hour')['count'].sum().plot()

df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

df[df['date_new'] == '2017-07-03']['weekday']
df['weekday'] = df['date_new'].apply(lambda x: x.weekday()+1)

df['weekday'].replace(7, 0, inplace=True)


for i in range(0,168,24):
    j = range()
    df.drop(df[df['weekday'] == (i/24) &
    (
    (df['hour'] < 1 | df['hour'] > 24)
    )
    ])
