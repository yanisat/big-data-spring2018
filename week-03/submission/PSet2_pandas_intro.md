# Problem Set 2: Intro to Pandas

Building off the in-class workshop, this problem set will require you to use some of Python's data wrangling functions and produce a few simple plots with Matplotlib. These plots will help us begin to think about how the aggregated GPS data works, how it might be useful, and how it might fall short.

## What to Submit

Create a duplicate of this file (`PSet2_pandas_intro.md`) in the provided 'submission' folder; your solutions to each problem should be included in the `python` code block sections beneath the 'Solution' heading in each problem section.

Be careful! We have to be able to run your code. This means that if you, for example, change a variable name and neglect to change every appearance of that name in your code, we're going to run into problems.

## Graphic Presentation

Make sure to label all the axes and add legends and units (where appropriate).

## Code Quality

While code performance and optimization won't count, all the code should be highly readable, and reusable. Where possible, create functions, build helper functions where needed, and make sure the code is self-explanatory.

## Preparing the Data

You'll want to make sure that your data is prepared using the procedure we followed in class. The code is reproduced below; you should simply be able to run the code and reproduce the dataset with well-formatted datetime dates and no erroneous hour values.

```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)
range(0,168,1)[-5]
# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
    )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)

    ```

## Problem 1: Create a Bar Chart of Total Pings by Date

Your first task is to create a bar chart (not a line chart!) of the total count of GPS pings, collapsed by date. You'll have to use `.groupby` to collapse your table on the grouping variable and choose how to aggregate the `count` column. Your code should specify a color for the bar chart and your plot should have a title. Check out the [Pandas Visualization documentation](https://pandas.pydata.org/pandas-docs/stable/visualization.html) for some guidance regarding what parameters you can customize and what they do.

### Solution

```python
df_pingsbydate = df.groupby('date')['count'].sum()
pingsbydateplot = df_pingsbydate.plot(kind='bar', title= 'GPS Pings by Date', color='purple')
pingsbydateplot.set_ylabel('Total daily GPS pings')
pingsbydateplot.set_xlabel('Date')
plt.show()
```

## Problem 2: Modify the Hours Column

Your second task is to further clean the data. While we've successfully cleaned our data in one way (ridding it of values that are outside the 24-hour window that correspond to a given day of the week) it will be helpful to restructure our `hour` column in such a way that hours are listed in a more familiar 24-hour range. To do this, you'll want to more or less copy the structure of the code we used to remove data from hours outside of a given day's 24-hour window. You'll then want to use the [DataFrame's `replace` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html). Note that you can use lists in both `to_replace` and `value`.

After running your code, you should have either a new column in your DataFrame or new values in the 'hour' column. These should range from 0-23. You can test this out in a couple ways; the simplest is probably to `df['hour'].unique()`; if you're interested in seeing sums of total pings by hour, you can run `df.groupby('hour')['count'].sum()`.

### Solution

```python
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df['hour'].replace(range(j, j + 5, 1), range(19, 24, 1), inplace=True)
    df['hour'].replace(range(i, i + 19, 1), range(0, 19, 1), inplace=True)
  else:
    df['hour'].replace(range(j, j + 5, 1), range(19, 24, 1), inplace=True)
    df['hour'].replace(range(j + 5, j + 24, 1), range(0, 19, 1), inplace=True)

df.groupby('hour')['count'].sum()
```

## Problem 3: Create a Timestamp Column

Now that you have both a date and a time (stored in a more familiar 24-hour range), you can combine them to make a single timestamp. Because the columns in a `pandas` DataFrames are vectorized, this is a relatively simple matter of addition, with a single catch: you'll need to use `pd.to_timedelta` to convert your hours columns to a duration.

### Solution

```python
df['timestamp'] = df['date_new'] + pd.to_timedelta(df['hour'], unit='h')

```

## Problem 4: Create Two Line Charts of Activity by Hour

Create two more graphs. The first should be a **line plot** of **total activity** by your new `timestamp` field---in other words a line graph that displays the total number of GPS pings in each hour over the course of the week. The second should be a **bar chart** of **summed counts** by hours of the day---in other words, a bar chart displaying the sum of GPS pings occurring across locations for each of the day's 24 hours.

### Solution

```python
pingsbytimestampline = df.groupby('timestamp')['count'].sum().plot(title='GPS Pings by Timestamp', color='blue')
pingsbytimestampline.set_ylabel('Total GPS pings')
pingsbytimestampline.set_xlabel('Timestamp')
plt.show()

pingsbyhoursbar = df.groupby('hour')['count'].sum().plot(kind='bar', title='GPS Pings by Hour', color='red')
pingsbyhoursbar.set_ylabel('Total GPS pings')
pingsbyhoursbar.set_xlabel('Hour')
plt.show()
```

## Problem 5: Create a Scatter Plot of Shaded by Activity

Pick three times (or time ranges) and use the latitude and longitude to produce scatterplots of each. In each of these scatterplots, the size of the dot should correspond to the number of GPS pings. Find the [Scatterplot documentation here](http://pandas.pydata.org/pandas-docs/version/0.19.1/visualization.html#scatter-plot). You may also want to look into how to specify a pandas Timestamp (e.g., pd.Timestamp) so that you can write a mask that will filter your DataFrame appropriately. Start with the [Timestamp documentation](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timestamps-vs-time-spans)!

```python
df.groupby('timestamp').count()
df_eight20170702 = df[df["timestamp"]=='2017-07-02 08:00:00']
df_eight20170702_scatter = df_eight20170702.plot.scatter(x='lon', y='lat', s=df_eight20170702['count'],title='GPS Pings by Location at 8AM on July 2, 2017')
df_eight20170702_scatter.set_ylabel('Latitude')
df_eight20170702_scatter.set_xlabel('Longitude')
plt.show()

df_thirteen20170710 = df[df["timestamp"]=='2017-07-10 13:00:00']
df_thirteen20170710_scatter = df_thirteen20170710.plot.scatter(x='lon', y='lat', s=df_thirteen20170710['count'],title='GPS Pings by Location at 1PM on July 10, 2017')
df_thirteen20170710_scatter.set_ylabel('Latitude')
df_thirteen20170710_scatter.set_xlabel('Longitude')
plt.show()

df_two20170729 = df[df["timestamp"]=='2017-07-29 02:00:00']
df_two20170729_scatter = df_two20170729.plot.scatter(x='lon', y='lat', s=df_two20170729['count'],title='GPS Pings by Location at 2AM on July 29, 2017')
df_two20170729_scatter.set_ylabel('Latitude')
df_two20170729_scatter.set_xlabel('Longitude')
plt.show()
```

## Problem 6: Analyze Your (Very) Preliminary Findings

For three of the visualizations you produced above, write a one or two paragraph analysis that identifies:
1. A phenomenon that the data make visible (for example, how location services are utilized over the course of a day and why this might by).
2. A shortcoming in the completeness of the data that becomes obvious when it is visualized.
3. How this data could help us identify vulnerabilities related to climate change in the greater Boston area.

1) GPS Pings By Date (Problem 1) - This graph of total GPS pings by date shows that the last eight days of the month have about 40% less GPS pings than the rest of the month. One possible explanation of this drop may be changes in people's cell phone usage. At the end of the month, it is possible that people are running out of data on their phone and therefore use their GPS system less, in order to conserve their data. However, a shortcoming of this data is that we only have one month's worth, so we cannot accurately predict why there is such a drop off. The data collection company may be at fault and had some sort of malfunction in that last week of the month. This data could help us identify vulnerabilities related to climate change in the greater Boston area through what days of the month are people historically out and about at a greater rate.

2) GPS Pings By Hour (Problem 4) - This graph of the total GPS pings by hour of the day shows lower usage between midnight and 6am, when compared to the rest of the day. This makes sense because there are less people using GPS devices in the middle of the night. A point of further investigation for this data is to look at 6pm, since the count is lower at 6pm when compared to its surrounding hours. It may also be interesting to look at how the data may differ within the hour, since the data does not contain minutes. This data is helpful in identifying vulnearabilities related to climate change since it shows what times each day people are more active. People tend to be at home at night, so they may be less affected by floods then than during the day when they are driving or walking around.

3) GPS Pings by Location at 8am on July 02, 2017 (Problem 5) - This graph essentially shows a map of the GPS pings at 8am on a certain day, with bigger blobs equaling more pings. The areas of Boston with more activity have bigger circles, such as downtown and the North End. One downfall of this visualization is that, unless the viewer zooms in a lot, the small pockets of inactivity cannot easily be viewed, especially when it is next to a big circle. This data can help us identify vulnerabilities related to climate change in the greater Boston area due to showing where in the city there are a lot of people at certain times of day, or where a climate disaster may have the greatest impact.
