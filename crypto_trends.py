import json
import os 
import pandas as pd
import requests
from pycoingecko import CoinGeckoAPI
import re
import matplotlib.pyplot as plt
from datetime import timedelta, datetime, date

# return a jason file of reddit/r/cryptocurrency page info
def get_reddit_post():
    subreddit = 'cryptocurrency'
    limit = 500
    timeframe = 'day' # hour, day, week, month, year, all
    listing = 'top' # controversial, best, hot, new, random, rising, top

    try:
        base_url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}"
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print("An Error Occured")
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
    previous_date = unique_date_list[-2]  # get the second-to-last date (previous)
    current_date = unique_date_list[-1]  # get the last date (current)

    # calculate the percentage difference
    for coin in df['coin'].unique():
        condition_previous = (df['date'] == previous_date) & (df['coin'] == coin)
        condition_current = (df['date'] == current_date) & (df['coin'] == coin)

        previous_price = df.loc[condition_previous, 'price'].values[0]
        current_price = df.loc[condition_current, 'price'].values[0]

        percentage_diff = ((current_price - previous_price) / previous_price) * 100

        # update the 'percent_dif' column for the current coin
        df.loc[condition_current, 'percent_dif'] = percentage_diff

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
