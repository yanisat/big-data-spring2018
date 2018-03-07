#PSet 3 Scraping and Cleaning Twitter Data
#Step 1 Collecting 2000 tweets
import jsonpickle
import tweepy
import pandas as pd
import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 2000,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
      all_tweets.to_json(out_file)
  return all_tweets

latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/tweetsPSet3.json'
t_max = 2000

tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

#Step 2 Cleaning data and location pie chart
    #Clean duplicates
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

    #Clean locations
    #I am only considering cities within a 5 mile radius of Eric's office, the rest is "other" since having a location in like California doesn't make sense for this exercise. The cities include Cambridge, Boston, Somerville, Malden, Everett, Chelsea, Medford, Watertown, and Brookline
for city in ['Boston', 'boston', 'Cambridge', 'cambridge', 'Somerville', 'somerville', 'Medford', 'medford', 'Malden', 'malden', 'Brookline', 'brookline', 'Watertown', 'watertown', 'Everett', 'everett', 'Chelsea', 'chelsea']:
    city_list = tweets[tweets['location'].str.contains(city)]['location']
    tweets['location'].replace(city_list, city.title() + ', MA', inplace = True)

for notcity in ['Dorchester', 'DORCHESTER', 'Brighton', 'Allston', 'Jamaica Plain', 'Roxbury', 'Bos', 'BOS', 'bos', 'Charlestown', 'charlestown']:
    actually_boston = tweets[tweets['location'].str.contains(notcity)]['location']
    tweets['location'].replace(actually_boston, 'Boston, MA', inplace = True)

    #In order to keep the 9 main cities and change all other locations to "other", mark the keep ones as keep
for city in ['Boston', 'Cambridge', 'Somerville', 'Malden', 'Everett', 'Chelsea', "Medford", 'Watertown', 'Brookline']:
    city_list = tweets[tweets['location'].str.contains(city)]['location']
    tweets['location'].replace(city_list, city + 'KEEP', inplace = True)
    #Change everything without "KEEP" in name into "other"
tweets['location'].replace(tweets[~tweets['location'].str.contains('KEEP')]['location'], 'other', inplace = True)
    #Remove "KEEP"
for city in ['Boston', 'Cambridge', 'Somerville', 'Malden', 'Everett', 'Chelsea', "Medford", 'Watertown', 'Brookline']:
    city_list = tweets[tweets['location'].str.contains(city)]['location']
    tweets['location'].replace(city_list, city + ', MA', inplace = True)
    #Check number of hits per location during cleaning
loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_sorted_count_tweets = df_count_tweets.sort_values('count')

    #Create a pie chart
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

plt.pie(df_sorted_count_tweets['count'], shadow=False)
plt.axis('equal')
plt.tight_layout()
plt.title("User Reported Locations of Tweets")
plt.legend(labels=df_sorted_count_tweets.index.get_values())
plt.show()

#Step 3 Scatterplot of geolocation
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.title('Geolocated Tweets')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#Step 4 Pick a search term
latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/snowtweetsPSet3.json'
t_max = 2000
search_for = 'snow'

snowtweets = get_tweets(
  geo = geocode_query,
  search_term = search_for,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

#Step 5 cleaning snow tweets
    #Clean duplicates
snowtweets.drop_duplicates(subset = 'content', keep = False, inplace = True)
    #Clean locations
    #I am only considering cities within a 5 mile radius of Eric's office, the rest is "other" since having a location in like California doesn't make sense for this exercise. The cities include Cambridge, Boston, Somerville, Malden, Everett, Chelsea, Medford, Watertown, and Brookline
for city in ['Boston', 'boston', 'Cambridge', 'cambridge', 'Somerville', 'somerville', 'Medford', 'medford', 'Malden', 'malden', 'Brookline', 'brookline', 'Watertown', 'watertown', 'Everett', 'everett', 'Chelsea', 'chelsea']:
    city_list = snowtweets[snowtweets['location'].str.contains(city)]['location']
    snowtweets['location'].replace(city_list, city.title() + ', MA', inplace = True)

for notcity in ['Dorchester', 'DORCHESTER', 'Brighton', 'Allston', 'Jamaica Plain', 'Roxbury', 'Bos', 'BOS', 'bos', 'Charlestown', 'charlestown']:
    actually_boston = snowtweets[snowtweets['location'].str.contains(notcity)]['location']
    snowtweets['location'].replace(actually_boston, 'Boston, MA', inplace = True)

    #In order to keep the 9 main cities and change all other locations to "other", mark the keep ones as keep
for city in ['Boston', 'Cambridge', 'Somerville', 'Malden', 'Everett', 'Chelsea', "Medford", 'Watertown', 'Brookline']:
    city_list = snowtweets[snowtweets['location'].str.contains(city)]['location']
    snowtweets['location'].replace(city_list, city + 'KEEP', inplace = True)
    #Change everything without "KEEP" in name into "other"
snowtweets['location'].replace(snowtweets[~snowtweets['location'].str.contains('KEEP')]['location'], 'other', inplace = True)
    #Remove "KEEP"
for city in ['Boston', 'Cambridge', 'Somerville', 'Malden', 'Everett', 'Chelsea', "Medford", 'Watertown', 'Brookline']:
    city_list = snowtweets[snowtweets['location'].str.contains(city)]['location']
    snowtweets['location'].replace(city_list, city + ', MA', inplace = True)
    #Check number of hits per location during cleaning
loc_snowtweets = snowtweets[snowtweets['location'] != '']
count_snowtweets = loc_snowtweets.groupby('location')['id'].count()
df_count_snowtweets = count_snowtweets.to_frame()
df_count_snowtweets.columns
df_count_snowtweets.columns = ['count']
df_sorted_snowcount_tweets = df_count_snowtweets.sort_values('count')

#Step 6 Scatterplot of snow tweets geolocation
snowtweets_geo = snowtweets[snowtweets['lon'].notnull() & snowtweets['lat'].notnull()]
len(snowtweets_geo)
len(snowtweets)
plt.scatter(snowtweets_geo['lon'], snowtweets_geo['lat'], s = 25)
plt.title('Geolocated Tweets About Snow')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#Step 7 export to csv
tweets.to_csv('submission/pset3.csv', sep=',', encoding='utf-8')
snowtweets.to_csv('submission/pset3_snow.csv', sep=',', encoding='utf-8')
