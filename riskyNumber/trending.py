#import psycopg2
#import feedparser
import pandas as pd
#import time
#from subprocess import check_output

import requests
from bs4 import BeautifulSoup as bs
from riskyNumber.models import Stock

def get_trending():
    nasdaq = 'http://www.nasdaq.com/markets/most-active.aspx'
    nyse = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=NYSE'
    amex = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=AMEX'
         
    mostActiveList = []
    mostAdvancedList = []
    mostDeclinedList = []    
    trendDict = {}

    response = requests.get(nasdaq)
    soup = bs(response.content, "lxml")    
    
    #activeStocks = response.css('div#_active a.mostactive')
    # mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    # mostActive = mostActive.find_all('h3')[1:2]
    mostAdvanced = mostAdvanced.find_all('h3')[1:13]
    mostDeclined = mostDeclined.find_all('h3')[1:13]
    
    # for h in mostActive:
    #     symbol = h.string
    #     mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        trendDict[symbol] = 'green'
        mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        trendDict[symbol] = 'red'
        mostDeclinedList.append(symbol)   
    
    ### NYSE
    response = requests.get(nyse)
    soup = bs(response.content, "lxml")    
    
    #mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    #mostActive = mostActive.find_all('h3')[1:1]
    mostAdvanced = mostAdvanced.find_all('h3')[1:5]
    mostDeclined = mostDeclined.find_all('h3')[1:5]
    
    # for h in mostActive:
    #     symbol = h.string
    #     mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        trendDict[symbol] = 'green'
        mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        trendDict[symbol] = 'red'
        mostDeclinedList.append(symbol)    
    
    ### AMEX
    response = requests.get(amex)
    soup = bs(response.content, "lxml")    
    
    #mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    #mostActive = mostActive.find_all('h3')[1:2]
    mostAdvanced = mostAdvanced.find_all('h3')[1:2]
    mostDeclined = mostDeclined.find_all('h3')[1:2]
    
    # for h in mostActive:
    #     symbol = h.string
    #     if Stock.objects.filter(ticker__iexact=symbol).exists():
    #         mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        if Stock.objects.filter(ticker__iexact=symbol).exists():
            trendDict[symbol] = 'green'
            mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        if Stock.objects.filter(ticker__iexact=symbol).exists():
            trendDict[symbol] = 'red'
            mostDeclinedList.append(symbol)    
       
    set1 = set(mostAdvancedList + mostDeclinedList)
    #set2 = set(mostActiveList)
    trendSet = set1 #set2.union(set1)    
    tikCikDf = pd.read_csv('tickerCik.txt', index_col = 0, dtype = {'CIK': str})
    symbols = set(tikCikDf.Symbol)
    
    #trendList = list(trendSet & symbols)
    trendDict= {k:v for k, v in trendDict.items() if k in symbols}
    
    return trendDict #trendList # mostActiveList, mostAdvancedList, mostDeclinedList