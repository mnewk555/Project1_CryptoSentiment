import panel as pn
pn.extension('plotly')
from panel.interact import interact
from panel import widgets
import plotly.express as px
import pandas as pd
import hvplot.pandas
import matplotlib.pyplot as plt
from pathlib import Path
from dotenv import load_dotenv #Just in case we need an API key.
import requests
import json
import numpy as np

from datetime import date
from datetime import timedelta
pd.options.display.float_format = '{:.5f}'.format

def fetch_daily_data(symbol, start, end):
    pair_split = symbol.split('/') # Splitting our symbol by the '/' and creating a a list for the new values.
    symbol = pair_split[0] + '-' + pair_split[1] # symbol = BTC-USD #The API request format requires the dash.
    url = f'https://api.pro.coinbase.com/products/{symbol}/candles?start={start}&end={end}&granularity=86400'#notice the symbol insert. There are 86400 seconds in a day.
    response = requests.get(url) #getting response from website
    if response.status_code == 200: # check to make sure the response from server is good
        #if response is good then we create a dataframe by reformatting a json load.
        data = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])
        data['date'] = pd.to_datetime(data['unix'], unit='s') # convert to a readable date
       #######

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            data.to_csv(f'Coinbase_{pair_split[0] + pair_split[1]}_dailydata_{end}.csv', index=False)
    else:
        print("Did not receieve OK response from Coinbase API")
        
today = date.today()
yesterday = today - timedelta(days = 1)
yesterday = yesterday.strftime("%Y-%m-%d")
#start_date = yesterday - timedelta(days = 300)#wont let me get more then 298 days, or so.
start_date = '2015-01-01'
end_date = '2015-09-30'
#start_date = start_date.strftime("%Y-%m-%d")
#end_date = end_date.strftime("%Y-%m-%d")
cryptolist = ['BTC/USD', 'ETH/USD', 'LTC/USD']

#function to pull crypto data from coinbase api passing in crypto symbol pair, start and end date,
def fetch_main_cryptos(crypto):
    fetch_daily_data(crypto, start_date, end_date)

    
#call the function calling our API loop thrgouh crypto list and pull based on start/end date
for crypto in cryptolist:
    fetch_main_cryptos(crypto)
    
BTC_path, ETH_path, LTC_path = (Path('../Justin_edits/Coinbase_BTCUSD_dailydata.csv'),
                                Path('../Justin_edits/Coinbase_ETHUSD_dailydata.csv'),
                                Path('../Justin_edits/Coinbase_LTCUSD_dailydata.csv'))
BTC_df, ETH_df, LTC_df = (pd.read_csv(BTC_path, index_col='date', infer_datetime_format=False, parse_dates=True),
                          pd.read_csv(ETH_path, index_col='date', infer_datetime_format=False, parse_dates=True),
                          pd.read_csv(LTC_path, index_col='date', infer_datetime_format=False, parse_dates=True))

#This function is to create our main datasets. Please edit and comment on how we should approach this.
#user, category, date, polarity, popularity, fav_count, volume, 
def clean_data(df):
    df = df.dropna() # immediately drop any null values
    df = df.drop(columns=['unix']).copy() #create deep copy of df with desired columns
    df['volume_change'] = df['volume'].pct_change() #find daily percent change in volume
    df['percent_volatility'] = round(((df['high'] - df['low']) / df['high']) * 100, 2) #Finding the amount of change between the low and high, then comparing it to the high.
    df['daily_change'] = round(df['close'].pct_change(), 5) # daily pct change
    df['daily_avg_price'] = round((df['open'] + df['close']) / 2, 2)
    df['rolling_volatility'] = round(df['percent_volatility'].rolling(30).mean(), 2)
    df['avg_volume_change'] = df['volume_change'].rolling(30).mean()
    df['rolling_volume'] = round(df['volume'].rolling(3).mean(), 2)
    df.drop(df.head(2).index, inplace=True) # drop the unfinished and upcoming day, inclusive of NA data
    df.drop(columns=['low', 'close', 'open'], inplace=True)
    df.round(decimals=2)
    df.sort_index(inplace=True)
    return pd.DataFrame(df)
def clean_new_data(df):
    return df.dropna()
#these are the base data sets so far
BTC_df = clean_data(BTC_df).dropna()
ETH_df = clean_data(ETH_df)
LTC_df = clean_data(LTC_df)

#joined columns into new dataframe and renamed
BTC_volume = BTC_df['volume']
ETH_volume = ETH_df['volume']
LTC_volume = LTC_df['volume']
volume_df = clean_new_data(pd.concat([BTC_volume, ETH_volume, LTC_volume], axis=1))
volume_df.columns = ['BTC_volume', 'ETH_volume', 'LTC_volume']

#joined columns into new dataframe and renamed
BTC_rolling_volume = BTC_df['rolling_volume']
ETH_rolling_volume = ETH_df['rolling_volume']
LTC_rolling_volume = LTC_df['rolling_volume']
rolling_volume_change_df = clean_new_data(pd.concat([BTC_rolling_volume, ETH_rolling_volume, LTC_rolling_volume], axis=1))
rolling_volume_change_df.columns = ['BTC_rolling_volume', 'ETH_rolling_volume', 'LTC_rolling_volume']


#joined columns into new dataframe and renamed
BTC_volume_change = BTC_df['volume_change']
ETH_volume_change = ETH_df['volume_change']
LTC_volume_change = LTC_df['volume_change']
volume_change_df = clean_new_data(pd.concat([BTC_volume_change, ETH_volume_change, LTC_volume_change], axis=1))
volume_change_df.columns = ['BTC_volume_change', 'ETH_volume_change', 'LTC_volume_change']

#joined columns into new dataframe and renamed
BTC_volatilityr = BTC_df['rolling_volatility']
ETH_volatilityr = ETH_df['rolling_volatility']
LTC_volatilityr = LTC_df['rolling_volatility']
volatilityr_df = clean_new_data(pd.concat([BTC_volatilityr, ETH_volatilityr, LTC_volatilityr], axis=1))
volatilityr_df.columns = ['BTC_rolling_volatility', 'ETH_rolling_volatility', 'LTC_rolling_volatility']

#joined columns into new dataframe and renamed
BTC_volatility = BTC_df['percent_volatility']
ETH_volatility = ETH_df['percent_volatility']
LTC_volatility = LTC_df['percent_volatility']
volatility_df = clean_new_data(pd.concat([BTC_volatility, ETH_volatility, LTC_volatility], axis=1))
volatility_df.columns = ['BTC_volatility', 'ETH_volatility', 'LTC_volatility']

#joined columns into new dataframe and renamed
BTC_high = BTC_df['high']
ETH_high = ETH_df['high']
LTC_high = LTC_df['high']
close_df = clean_new_data(pd.concat([BTC_high, ETH_high, LTC_high], axis=1))
close_df.columns = ['BTC_high', 'ETH_high', 'LTC_high']
ETH_LTC_close_df = clean_new_data(close_df.drop(columns='BTC_high'))

#joined columns into new dataframe and renamed
BTC_daily_change = BTC_df['daily_change']
ETH_daily_change = ETH_df['daily_change']
LTC_daily_change = LTC_df['daily_change']
daily_change_df = clean_new_data(pd.concat([BTC_daily_change, ETH_daily_change, LTC_daily_change], axis=1))
daily_change_df.columns = ['BTC_daily_change', 'ETH_daily_change', 'LTC_daily_change']

twitter_path = Path('../data/raw_data/raw_tweets_01_filter_polarity.csv')
twitter_df = pd.read_csv(twitter_path, infer_datetime_format=True, parse_dates=True)
datetime = twitter_df['time'].str.split(" ", n=1, expand = True)
twitter_df['date'] = datetime[0]
twitter_df.drop(columns='time')
twitter_df['time'] = datetime[1]
twitter_df.drop_duplicates(subset='text', inplace=True)
twitter_df.set_index('date', inplace=True)
#TODO: round all columns
df = pd.merge(twitter_df, volume_change_df, how='inner', left_index=True, right_index=True)
df2 = pd.merge(df, volatility_df, how='inner', left_index=True, right_index=True)
df3 = pd.merge(df2, close_df, how='inner', left_index=True, right_index=True)
df4 = pd.merge(df3, volatilityr_df, how='inner', left_index=True, right_index=True)
df5 = pd.merge(df4, rolling_volume_change_df, how='inner', left_index=True, right_index=True)
df6 = pd.merge(df5, volume_df, how='inner', left_index=True, right_index=True)
twitter_analysis_df = pd.merge(df6, daily_change_df, how='inner', left_index=True, right_index=True)
twitter_analysis_df['Popularity Rating'] = round(twitter_analysis_df['Popularity Rating'], 2)
twitter_analysis_df.sort_index(inplace=True)
twitter_analysis_df['category'].fillna('null', inplace=True)

#tweet_analysis_df['2020-03-30':'2021-19-01']
#df1.merge(df2, on='ID', how='left')
def export_df(df):
    return df.to_csv('../data/raw_data/raw_crypto_data.csv')
export_df(twitter_analysis_df)

twitter_users = twitter_analysis_df['twitter_user'].unique()
crypto_category = twitter_analysis_df['category'].unique()
crypto_category
bitcoin_tweets_df = twitter_analysis_df[twitter_analysis_df['category'].str.contains('bit')]
ethereum_tweets_df = twitter_analysis_df[twitter_analysis_df['category'].str.contains('eth')]
twitter_users

avg_df = twitter_analysis_df[twitter_analysis_df['category'] == 'bitcoin']

elon = twitter_users[5]
elon_tweets_df = twitter_analysis_df[twitter_analysis_df['twitter_user'] == elon]
elon_tweet1 = elon_tweets_df[elon_tweets_df['Popularity Rating'] != 0]
elon_tweets_rated = elon_tweets_df[elon_tweets_df['category'] == 'bitcoin']
elon_tweets_rated.drop(columns=['sentiment', 'time', 'tweet_id', 'tweet_source', 'quote_count', 'reply_count', 'retweet_count'], inplace=True)

def practice():
    return elon_tweets_rated.hvplot.scatter(x='date', y='Popularity Rating', width=1000, height=500, yformatter='%.0f', legend='left') * elon_tweets_rated.hvplot.line(x='date', y='BTC_rolling_volume', legend='left') * elon_tweets_rated.hvplot.area(x='date', y='BTC_volume', stacked=False, legend='left')