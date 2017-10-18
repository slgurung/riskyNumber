import urllib
import datetime as dt
import pandas as pd
from pandas_datareader import data as web
import pandas_datareader as pdr
#import requests
#import matplotlib.pyplot as plt

def get_google_data(symbol, period, window, exch = 'NASDAQ'):
    url_root = ('http://www.google.com/finance/getprices?i='
                + str(period) + '&p=' + str(window)
                + 'd&f=d,o,h,l,c,v&df=cpct&x=' + exch.upper() 
                + '&q=' + symbol.upper())
    
    response = urllib.request.urlopen(url_root)
    data=response.read().decode().split('\n')       #decode() required for Python 3
    #d=data
    data = [data[i].split(',') for i in range(len(data)-1)]
    
    header = data[0:7]
    
    data = data[7:]
    header[4][0] = header[4][0][8:]  
                             #get rid of 'Columns:' for label row
    df=pd.DataFrame(data, columns=header[4])
      
    ind=pd.Series(len(df))
    for i in range(len(df)):
        if df['DATE'].ix[i][0] == 'a':
            anchor_time = dt.datetime.fromtimestamp(int(df['DATE'].ix[i][1:]))  #make datetime object out of 'a' prefixed unix timecode
            ind[i]=anchor_time
        else:
            ind[i] = anchor_time +dt.timedelta(seconds = (period * int(df['DATE'].ix[i])))
         
    df.index = ind
    
    df=df.drop('DATE', 1)

    for column in df.columns:    #shitty implementation because to_numeric is pd but does not accept df
        df[column]=pd.to_numeric(df[column])
    
    df.columns = df.columns.str.lower()
    return df
    
def get_yahoo_intraday(ticker, day ): #day need to be 1 for this function, instead us get_intraday()
    
    url_root = ('http://chartapi.finance.yahoo.com/instrument/1.0/'
                + ticker.upper() + '/chartdata;type=quote;range='
                + str(day) + 'd/csv')
    
    #url_root = ('http://download.finance.yahoo.com/d/quotes.csv?s=CYTR&f=abof6')
    
    response = urllib.request.urlopen(url_root)
    
    data=response.read().decode().split('\n')   #decode() required for Python 3
    
    data = [data[i].split(',') for i in range(len(data)-1)]
    
    header = data[11]
    data = data[17:]
    header[0] = 'date'               #get rid of 'Columns:' for label row
    df=pd.DataFrame(data, columns=header)
    
    ind=pd.Series(len(df))
    for i in range(len(df)):
        anchor_time = dt.datetime.fromtimestamp(int(df['date'].ix[i]))  #make datetime object out of 'a' prefixed unix timecode
        ind[i]= anchor_time
        #ind[i] = anchor_time + dt.timedelta(seconds = (day * int(df['date'].ix[i])))
        
    df.index = ind
    df=df.drop('date', 1)
    
    return df
    

def get_intraday(ticker, day=1):
        
    if (day == 1):
        url_root = ('http://chartapi.finance.yahoo.com/instrument/1.0/'
                + ticker.upper() + '/chartdata;type=quote;range=1d/csv')
    
        #url_root = ('http://download.finance.yahoo.com/d/quotes.csv?s=CYTR&f=abof6')
    
        response = urllib.request.urlopen(url_root)
        
        data=response.read().decode().split('\n')   #decode() required for Python 3
        data = [data[i].split(',') for i in range(len(data)-1)]
    
        header = data[11]
        data = data[17:]
        header[0] = 'date'               #get rid of 'Columns:' for label row
        df=pd.DataFrame(data, columns=header)
        '''
        ind=pd.Series(0)
        for i in range(len(df)):
            anchor_time = dt.datetime.fromtimestamp(int(df['date'].ix[i]))  #make datetime object out of 'a' prefixed unix timecode
            ind[i]= anchor_time
            #ind[i] = anchor_time + dt.timedelta(seconds = (day * int(df['date'].ix[i])))
        
        df.index = ind
        df=df.drop('date', 1)
        '''
    else:
        url_root = ('http://chartapi.finance.yahoo.com/instrument/1.0/'
                + ticker.upper() + '/chartdata;type=quote;range='
                + str(day) + 'd/csv')
    
        #url_root = ('http://download.finance.yahoo.com/d/quotes.csv?s=CYTR&f=abof6')
    
        response = urllib.request.urlopen(url_root)
        data=response.read().decode().split('\n')   #decode() required for Python 3
        data = [data[i].split(',') for i in range(len(data)-1)]
        
        header = data[16]
        data = data[22:]
        header[0] = 'date'               #get rid of 'Columns:' for label row
        df=pd.DataFrame(data, columns=header)
        '''
        ind=pd.Series(0)
        
        for i in range(len(df)):
            anchor_time = dt.datetime.fromtimestamp(int(df['date'].ix[i]))  #make datetime object out of 'a' prefixed unix timecode
            ind[i]= anchor_time
            #ind[i] = anchor_time + dt.timedelta(seconds = (day * int(df['date'].ix[i])))
        
        df.index = ind
        df=df.drop('date', 1)
        '''
    
    return df



#df = get_google_data('FB', 60, 1, 'NASDAQ')

# one week historical data 
def get_historical(ticker, period = 1825):
    
    if dt.datetime.now().hour > 16:
        end = dt.date.today()
        start = end - dt.timedelta(period - 1)
    else:
        end = dt.date.today() - dt.timedelta(1)
        start = end - dt.timedelta(period)
    
    #quote = web.DataReader(ticker, data_source='yahoo', start=start, end=end)
    quote = pdr.get_data_yahoo(ticker, start=start, end=end)
    quote.columns = quote.columns.str.lower()

    return quote   

def yahoo_info(tik):
    url = ('http://finance.yahoo.com/quote/'
           + tik + '/key-statistics?p=' + tik)
    response = urllib.request.urlopen(url)
    
    data=response.read().decode().split(',')
    
    return data # didn't work
def get_time_range():
    today = dt.date.today()
    start = dt.datetime(today.year, today.month, today.day, 9, 30, 0)
    end = dt.datetime(today.year, today.month, today.day, 16, 0, 0)
    step = dt.timedelta(minutes = 1)
    timeList = []
    while start <= end:
        #yield start
        timeList.append(str(start))
        start += step
    return timeList, [0] * len(timeList)
    
