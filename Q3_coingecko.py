import datetime
from urllib import response
from pycoingecko import CoinGeckoAPI
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

""" Please note that the ranking of the tokens is based on the search volume on CoinGecko's platform by users in the 
last 24 hours. One can also use CoinGecko's API to get the top 7 most trending coins, but in order to get the top 10 most 
trending coins, I extract data from their 'Discover' page, where CoinGecko lists the top trending tokens. 
Then, I use CoinGecko's API to obtain the 24h Volume and Market Cap of the tokens. As it is a dynamic ranking and changes 
over time, the ranking that I have generated is for a given point of time, which is mentioned at the title of the table and 
the name of the csv file."""


cg = CoinGeckoAPI()

base_url = "https://www.coingecko.com/en/discover"

response = requests.get(base_url)

soup = BeautifulSoup(response.content, 'html.parser')

card_body = soup.findAll("div", {'class': 'card-body'})
coin_list = cg.get_coins_list()
coin_names = []
market_cap =[]
volume = []


for i in card_body:
    h5 = i.find("h5", {'class': 'card-title mb-4'})
    title = h5.get_text()
    if title == "Trending Search":
        coin_links = i.findAll('a')
        for link in coin_links:
            y = link.find('span')
            name = y.get_text()
            coin_names.append(name)
            coin_id = str
            for coin in coin_list:
                if coin['name'] == name:
                    coin_id = coin['id']
            print(coin_id, name)
            data = cg.get_coin_market_chart_by_id(id = coin_id, vs_currency = 'usd',days = 2)
            mcap = data['market_caps'][-1][-1]
            market_cap.append(mcap)
            vol = data['total_volumes'][-1][-1]
            volume.append(vol)
 
df = pd.DataFrame()
df['rank'] = range(1,16)
df['name'] = coin_names
df['market_cap_USD'] = market_cap
df['24_h_volume_USD'] = volume
df = df[:10]

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = dir_path+'/Q3_crypto_ranking_{}.csv'.format(datetime.datetime.now())
df.to_csv(file_path, index = False)
