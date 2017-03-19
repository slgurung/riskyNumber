#import psycopg2
#import feedparser
#import pandas as pd
#import time
#from subprocess import check_output

import requests
from bs4 import BeautifulSoup as bs

def get_trending():
    nasdaq = 'http://www.nasdaq.com/markets/most-active.aspx'
    nyse = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=NYSE'
    amex = 'http://www.nasdaq.com/markets/most-active.aspx?exchange=AMEX'
         
    mostActiveList = []
    mostAdvancedList = []
    mostDeclinedList = []    
    
    response = requests.get(nasdaq)
    soup = bs(response.content, "lxml")    
    
    #activeStocks = response.css('div#_active a.mostactive')
    mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    mostActive = mostActive.find_all('h3')[1:4]
    mostAdvanced = mostAdvanced.find_all('h3')[1:5]
    mostDeclined = mostDeclined.find_all('h3')[1:6]
    
    for h in mostActive:
        symbol = h.string
        mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        mostDeclinedList.append(symbol)   
    
    ### NYSE
    response = requests.get(nyse)
    soup = bs(response.content, "lxml")    
    
    mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    mostActive = mostActive.find_all('h3')[1:1]
    mostAdvanced = mostAdvanced.find_all('h3')[1:2]
    mostDeclined = mostDeclined.find_all('h3')[1:2]
    
    for h in mostActive:
        symbol = h.string
        mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        mostDeclinedList.append(symbol)    
    
    ### AMEX
    response = requests.get(amex)
    soup = bs(response.content, "lxml")    
    
    mostActive = soup.find('div', id='_active')
    mostAdvanced = soup.find('div', id='_advanced')
    mostDeclined = soup.find('div', id='_declined')
    #print(mostAdvanced.prettify())
    mostActive = mostActive.find_all('h3')[1:2]
    mostAdvanced = mostAdvanced.find_all('h3')[1:2]
    mostDeclined = mostDeclined.find_all('h3')[1:2]
    
    for h in mostActive:
        symbol = h.string
        mostActiveList.append(symbol)
    for h in mostAdvanced:
        symbol = h.string
        mostAdvancedList.append(symbol)
    for h in mostDeclined:
        symbol = h.string
        mostDeclinedList.append(symbol)    
       
    set1 = set(mostAdvancedList + mostDeclinedList)
    set2 = set(mostActiveList)
    trendList = set2.union(set1)    
    
    
    
    return list(trendList) # mostActiveList, mostAdvancedList, mostDeclinedList