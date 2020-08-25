from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import datetime as dt
import pymysql

def get_bid_asks_usd():
    url = 'https://www.arionbanki.is/'
    response = requests.get(url)
    page_soup = BeautifulSoup(response.content, 'lxml')
    bids = page_soup.find_all('td', class_="currency-changer__buy")
    asks = page_soup.find_all('td', class_="currency-changer__sell")
    ans = []

    for i in range(1, 10):
        bid = float(bids[i].get_text())
        ask = float(asks[i].get_text())
        mid = round((bid+ask)/2, 2)
        ans.append(bid)
        ans.append(ask)
        ans.append(mid)

    return ans

def get_cur_index():
    url = 'https://www.m5.is/?gluggi=gjaldmidill&id=22'
    response = requests.get(url)
    page_soup = BeautifulSoup(response.content, 'lxml')
    get_currency_div = page_soup.find_all('div', class_="span6")
    ind = get_currency_div[0].find_all('div')[0].get_text()
    return float(ind.replace(',','.'))

def get_currency_quotes():
    df = pd.DataFrame({})
    df['time'] = ""
    df['USD bid'] = ""
    df['USD ask'] = ""
    df['USD mid'] = ""
    df['GBP bid'] = ""
    df['GBP ask'] = ""
    df['GBP mid'] = ""
    df['EUR bid'] = ""
    df['EUR ask'] = ""
    df['EUR mid'] = ""
    df['PLN bid'] = ""
    df['PLN ask'] = ""
    df['PLN mid'] = ""
    df['DKK bid'] = ""
    df['DKK ask'] = ""
    df['DKK mid'] = ""
    df['NOK bid'] = ""
    df['NOK ask'] = ""
    df['NOK mid'] = ""
    df['SEK bid'] = ""
    df['SEK ask'] = ""
    df['SEK mid'] = ""
    df['CAD bid'] = ""
    df['CAD ask'] = ""
    df['CAD mid'] = ""
    df['AUD bid'] = ""
    df['AUD ask'] = ""
    df['AUD mid'] = ""
    df['cur_ind'] = ""
    counter = 0
    current_time = dt.datetime.now()
    five_pm = dt.datetime(current_time.year, current_time.month, current_time.day, 16, 0, 0)
    while True:
        if current_time >= five_pm:
            break
        ans = get_bid_asks_usd()
        current_time = dt.datetime.now()
        ind = get_cur_index()
        df.loc[counter] = [current_time] + ans + [ind]
        print (df[['USD bid', 'USD mid','USD ask']])
        counter += 1
        time.sleep(60)
    return df
