#!/usr/bin/python3
import json
import os 
import pandas as pd
import requests
from pycoingecko import CoinGeckoAPI
import re
import matplotlib.pyplot as plt
from datetime import timedelta, datetime, date

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# return a jason file of reddit/r/cryptocurrency page info
def get_reddit_post():
    subreddit = 'cryptocurrency'
    limit = 500
    timeframe = 'day' # hour, day, week, month, year, all
    listing = 'top' # controversial, best, hot, new, random, rising, top

    try:
        base_url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}"
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
        request.raise_for_status()  # Raises an exception for HTTP errors (4xx and 5xx)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Exception: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        return request.json()

# create a json file of the first 250 pages of cryptocurrency from coin gecko
def get_coin_prices():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', per_page=250)
    with open('coinListWithPrices.json', 'w') as jason_file:
        json.dump(coins, jason_file, indent=4)  

# use coingecko json file to see if a coin is mentioned on reddit crypto sub
def check_if_coin_in_post(reddit_post):
    coin_result_data = {}
    
    with open('coinListWithPrices.json', 'r') as jason_file:
        coinList = json.load(jason_file)
              
    # if coin is in reddit title, create a dictionary with the coin info (name, price, time of retrieval)
    for post in reddit_post['data']['children']:
        for coin in coinList:
            coin_name = coin["name"]
            reddit_title = post['data']['title']
            # if coin found create dict entry with coin and price (account for spaces and punctuation)
            if re.search(coin_name + r'[ |.|!|,]', reddit_title, re.IGNORECASE) or re.search(coin['id'] + r'[ |.|!|,]', reddit_title, re.IGNORECASE):
                if coin_name not in coin_result_data:            
                    coin_result_data[coin_name] = {'price': coin['current_price'], 'date': datetime.now().strftime("%Y/%m/%d, %H:%M"), 'percent_dif': 0.0}   

    # create a csv file using data
    create_csv_for_chart(coin_result_data)

# create csv file from converting csv file to dataframe
def create_csv_for_chart(coin_result_data):
    # create a data frame from coin dictionaries
    df = pd.DataFrame.from_dict(coin_result_data, orient='index')
    df.index.name = 'coin'
    df.reset_index(inplace=True)
    
    # ouput data frame to csv file
    file_path = 'results_output.csv'
    if os.path.exists(file_path):
        df.to_csv('results_output.csv', mode='a', header=False, index=False)
    else:    
        df.to_csv('results_output.csv', index=False)

# calculate the percentage increase or deacrease from the previous time the script was run
def calculate_price_difference_percentage():
    df = pd.read_csv('results_output.csv')
    unique_date_list = df['date'].unique()

    # If not enough date data, set to none
    if len(unique_date_list) >= 2:
        previous_date = unique_date_list[-2]  # get the second-to-last date (previous)
    else:
        previous_date = None
    if len(unique_date_list) >= 1:
        current_date = unique_date_list[-1]  # get the last date (current)
    else:
        current_date = None

    for coin in df['coin'].unique():
        # If not enough date data, use default 0.0 for percentage change
        if previous_date == None or current_date == None:
            break
        else:
            condition_previous = (df['date'] == previous_date) & (df['coin'] == coin)
            condition_current = (df['date'] == current_date) & (df['coin'] == coin)

            # If a condition is true
            if len(condition_previous) > 0 and len(condition_current) > 0:
                previous_price = df.loc[condition_previous, 'price'].values[0]
                current_price = df.loc[condition_current, 'price'].values[0]

                percentage_diff = ((current_price - previous_price) / previous_price) * 100

                # update the 'percent_dif' column for the current coin
                df.loc[condition_current, 'percent_dif'] = percentage_diff
                
            # if the condition is false (coin no longer on reddit page, set to 0)
            else:
                # update the 'percent_dif' column for the current coin
                df.loc[condition_current, 'percent_dif'] = 0.0

    df.to_csv('results_output.csv', index=False)

# create a chart from csv that contains coin info
def create_chart():
    prices = []
    df = pd.read_csv('results_output.csv')

    # iterate through unique coins and plot a line for each
    for coin in df['coin'].unique():
        coin_data = df[df['coin'] == coin]
        plt.plot(coin_data['date'], coin_data['percent_dif'], marker='o', linestyle='-', label=coin)
        prices.extend(coin_data['percent_dif'].values.tolist())

    # create labels and legend
    plt.xlabel('Date')
    plt.ylabel('Percentage Change')
    plt.title('Percentage Change Over Time For Crypto Currently on /r/cryptocurrency')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.ylim(None, None)

    # rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # show the plot
    plt.tight_layout()
    plt.show()

def main():
    get_coin_prices()
    check_if_coin_in_post(get_reddit_post())
    calculate_price_difference_percentage()
    create_chart()

if __name__ == "__main__":
    main()
