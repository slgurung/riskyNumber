#import psycopg2
#import feedparser
#import pandas as pd
#import time
#from subprocess import check_output
#import sys
import requests
from bs4 import BeautifulSoup as bs
#import sqlite3
#import lxml 
#conn = sqlite3.connect('secfillings.db')
#cur = conn.cursor()
#tikCikDict = {}
#conn = psycopg2.connect(database="mydb", user="postgres", password="stocksql", host="localhost", port="5432")
#cur = conn.cursor()

def get_fillings(cik):
    
    '''
    if not tikCikDict:  #working this for setting global variable
        tikCikDf = pd.read_csv('tickerCik.txt', index_col = 0, dtype = {'CIK': str})
        tikCikDict = dict(zip(list(tikCikDf.Symbol), list(tikCikDf.CIK)))
        #tikCikDict['cik'] = '320193'1326801
        print('setting cik')
    '''
    #cik = str(tikCikDict[ticker.upper()]) # need to use str to make nan to 'nan'
    #if cik != 'nan':
    
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + str(cik)
    url += '&type=&dateb=&owner=include&count=10'
        
    response = requests.get(url)
    soup = bs(response.content, "lxml")    
    table = soup.find('table', class_='tableFile2') 
    rows = table.find_all('tr')
    
    form = []
    documentUrl = []
    description = []
    fillingDate = []
    
    for i in range(1, len(rows)):
        cells = rows[i].find_all('td')
        formName = 'Form ' + cells[0].string 
        form.append(formName)   
            
        docUrl = 'https://www.sec.gov' + cells[1].find('a')['href']
        doc = requests.get(docUrl)
        doc = bs(doc.content, "lxml")
        docTable = doc.find('table', class_='tableFile')
        docRow = docTable.find_all('tr')[1]
        docUrl = 'https://www.sec.gov'+ docRow.find('a')['href']
        documentUrl.append(docUrl)
            
        des = list(cells[2].strings)[0]
        description.append(des)
            
        fDate = cells[3].string.split(' ')[0]
        fillingDate.append(fDate)
            
        
    return form, documentUrl, description, fillingDate