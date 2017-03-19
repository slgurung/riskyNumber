import pandas as pd
#import numpy as np
#from pandas_datareader import data as web
#import datetime, re

import os #, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
                      'riskyNumberProject.settings')

import django

django.setup()
from riskyNumber.models import Exchange, Stock 

def add_ticker(ex, t, c, n, s, i): 
    tic = Stock.objects.get_or_create(exchange=ex, ticker=t, cik=c, name = n, sector = s, industry = i)[0] 
    tic.save() 

for e in ['NASDAQ', 'AMEX', 'NYSE']: 
    c = Exchange.objects.get_or_create(name=e)[0] 
    c.save() 
    

#tickerDf = pd.read_csv('tickerList.txt', index_col = 0)
#cikDf = pd.read_csv('tickercik.txt', index_col = 0)
tikCikDf = pd.read_csv('tikCikDf.txt', index_col = 0, na_values = ['', 'NaN'], dtype = {'CIK': str})

stockNum = len(tikCikDf)

for i in range(stockNum): 
    #if (re.match(r'^[\w]+$', tickerDf.ix[i, 0])): 
    ex = Exchange.objects.get_or_create(name = tikCikDf.ix[i, 'Exchange'])[0] 
    add_ticker(ex, tikCikDf.ix[i, 0], tikCikDf.ix[i, 5], tikCikDf.ix[i, 1], tikCikDf.ix[i, 2], tikCikDf.ix[i, 3]) 
         
            
'''
    for c in Exchange.objects.all(): 
        for p in Stock.objects.filter(category=c): 
            print("- {0} - {1}".format(str(c), str(p)))
            
'''

    













    

