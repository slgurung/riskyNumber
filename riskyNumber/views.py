#######################
from threading import Thread
from math import pi
import pandas as pd
import numpy as np
from pandas_datareader import data as web
import pandas_datareader as pdr
import feedparser
from datetime import datetime as dt
from datetime import date, timedelta

from yahoo_finance import Share as yf

#####################################

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from riskyNumber.intradayData import get_intraday, get_google_data, get_historical
from riskyNumber.fillings import get_fillings
from riskyNumber.trending import get_trending
from riskyNumber.models import Exchange, Stock, UserProfile, Trending
from riskyNumber.forms import UserForm, UserProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

# to store quote locally ##########
indexTicker = '^DJI' 
indexDf = get_historical(indexTicker)

updateQuote = True

stkQuote = {} 
#########################################
# to scrape sec fillings
tikCikDict = {}
if not tikCikDict:
    tikCikDf = pd.read_csv('tickerCik.txt', index_col = 0, dtype = {'CIK': str})
    tikCikDict = dict(zip(list(tikCikDf.Symbol), list(tikCikDf.CIK)))
###########################################

fillingDict={}

### to delete all stocks from database ###
#Stock.objects.all().delete()
##########################################

####### do something for begining setup
#trendList = []

# **At the beginning Need to disable this block before database is initialized
# Trending.objects.all().delete()
trendList = get_trending()
updateTrend = True
### to save trendList in database
# for t in trendList:
#     trendStk = Trending(ticker = t)
#     trendStk.save()
#*****************************************

indexTickerList = ['^GSPC', '^DJI', '^IXIC']
stkIndex = {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones Industrial' , '^IXIC': 'Nasdaq Composite'}
# for google finance url
#stkIndex = {'.INX': 'S&P 500', '.DJI': 'Dow Jones Industrial' , '.IXIC': 'Nasdaq Composite'}
#indexEx = {'.INX': 'INDEXSP', '.DJI': 'INDEXDJX' , '.IXIC': 'INDEXNASDAQ'}

def about(request):
    
    context_dict = {}
    context_dict['ticker'] = 1234 # to exclude resizeChart() on window resize
    context_dict['trending'] = list(trendList.keys())
    context_dict['trendType'] = list(trendList.values())    
    
    return render(request, 'riskyNumber/about.html', context_dict)

def index(request):
    global updateQuote
    global indexDf
    global trendList
    global updateTrend
    #global indexTicker

    context_dict = {}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    #################
    quotePeriod = 365 # need to match to chartPeriod at index.html

    ######## to store quote locally
    current_hour = dt.now().hour
    if current_hour > 16:
        if updateQuote:
            updateQuote = False # do I need to use globally to update globally???
            indexDf = get_historical(indexTicker)
        startDate = date.today() - timedelta(quotePeriod - 1)
        quote = indexDf[startDate: ]        
    else:
        updateQuote = True 
        startDate = date.today() - timedelta(quotePeriod)
        quote = indexDf[startDate: ]

    if current_hour > 11:
        if updateTrend:
            trendList = get_trending() # update trendList
            updateTrend = False
    else:
        updateTrend = True

    context_dict['trending'] = list(trendList.keys())
    context_dict['trendType'] = list(trendList.values())

    context_dict['ticker'] = indexTicker    
    context_dict['name'] = stkIndex[indexTicker]
    
       
    #context_dict['summary'], context_dict['fundamentals'] = get_summary(indexTicker)   
    
    i = list(quote.index.strftime("%Y-%m-%d"))
    
    context_dict['date'] = i #list(dateSeries.map(str)) # change Timestamp obj to string. but don't work strftime()
           
    context_dict['close'] = list(quote['adj close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    
    minClose = min(context_dict['close']) # min() is build-in fn
    context_dict['max'] = max(context_dict['high']) 
    
    context_dict['min'] = minClose - ((context_dict['max'] - minClose) * .25)

    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    
    y = (max(context_dict['low']) + quote.high.min()) * 0.5 
    x = context_dict['min'] * 0.9 + minClose * 0.1
       
    context_dict['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  
    
    context_dict['realVol'] = list(quote.volume)
    context_dict['businessNews'], context_dict['stockNews'] = news(indexTicker) # save this for quick download
   
    return render(request, 'riskyNumber/index.html', context_dict) # 'riskyNumber/index.html' is template location not url

def summary(request, ticker):
    #exchange = 'NASDAQ'
    global stkQuote  # to update stkQuote values
    quotePeriod = 365 # need to match with chartPeriod at summary.html
    context_dict = {}

    if ticker == indexTicker:
        #startDate = date.today() - timedelta(quotePeriod)
        quote = indexDf #[startDate: ]
    else:
        #if ticker not in stkQuote.keys(): #stkQuote['ticker'] != ticker:
        stkQuote[ticker] = get_historical(ticker)
        # else:
        #     quote = stkQuote[ticker] #get_historical(ticker)
        #stkQuote['ticker'] = ticker

        startDate = date.today() - timedelta(quotePeriod)
        quote = stkQuote[ticker][startDate: ]


    context_dict['trending'] = list(trendList.keys())
    context_dict['trendType'] = list(trendList.values())

    context_dict['ticker'] = ticker
                
    if ticker not in indexTickerList: #['^GSPC', '^DJI', '^IXIC']:
        context_dict['summary'], context_dict['fundamentals'] = get_summary(ticker)

        stkObj = Stock.objects.get(ticker = ticker).name.split(" ")[:2] # no error if list has one element
        if len(stkObj) > 1:
            context_dict['name'] = stkObj[0] + " " +stkObj[1]
        else:
            context_dict['name'] = stkObj[0]

        if ticker not in fillingDict.keys():
            fThread = fillingThread('filling:' + ticker, ticker)
            fThread.start()
    else:
        context_dict['name'] = stkIndex[ticker]
        #exchange = indexEx[ticker]
    # moved above inside if block
    # if ticker not in stkIndex.keys() and ticker not in fillingDict.keys():
    #     fThread = fillingThread('filling:' + ticker, ticker)
    #     fThread.start()
    
    # moved inside above if block
    # if ticker not in ['^DJI', '^IXIC', '^GSPC']:
    #     context_dict['summary'], context_dict['fundamentals'] = get_summary(ticker)   
    
    
    i = list(quote.index.strftime("%Y-%m-%d"))

    context_dict['date'] = i #list(dateSeries.map(str)) # change Timestamp obj to string. but don't work strftime()
    
    context_dict['close'] = list(quote['adj close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    #context_dict['vol'] = pd.to_numeric(quote.volume)

    minClose = min(context_dict['close']) # min() is build-in fn
    
    context_dict['max'] = max(context_dict['high']) 
    context_dict['min'] = minClose - ((context_dict['max'] - minClose) * .25)


    maxVol = quote.volume.max() # quote.volume is Series and use series fn max()
    minVol = quote.volume.min()

    y = (max(context_dict['low']) + quote.high.min()) * 0.5 #quote['adj close'].max() #quote.high.min() 
    x = context_dict['min'] * 0.9 + minClose * 0.1
       
    context_dict['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  
    
    context_dict['realVol'] = list(quote.volume) 
        
    context_dict['businessNews'], context_dict['stockNews'] = news(ticker) # save this for quick download
    context_dict['indexTickerList']  = indexTickerList

    return render(request, 'riskyNumber/summary.html', context_dict)

def hChart(request):    
    data = {}
    chartPeriod = request.POST.get('chartPeriod')
    ticker = request.POST.get('ticker')
    
    
    ##**** change this one
    if ticker == indexTicker:
        startDate = date.today() - timedelta(int(chartPeriod))
        quote = indexDf[startDate: ]
        
    else:
        startDate = date.today() - timedelta(int(chartPeriod))
        quote = stkQuote[ticker][startDate: ]
        #quote = get_historical(ticker, int(chartPeriod))
    # volume is int64 type and it is not json serializable
    # So, it need to convert to float type to make json serializable    
    quote.volume = quote.volume.astype('float64')

    data['dateVal'] = list(quote.index.strftime("%Y-%m-%d"))       
    data['ticker'] = ticker
    data['close'] = list(quote['adj close'])
    data['open'] = list(quote.open)
    data['high'] = list(quote.high)
    data['low'] = list(quote.low)
    
    minClose = min(data['close']) # min() is build-in fn
    data['max'] = max(data['high']) 
    data['min'] = minClose - ((data['max'] - minClose) * .25)

    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    y = (max(data['low']) + quote.high.min()) * 0.5 
    x = data['min'] * 0.9 + minClose * 0.1
   
    data['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  
    
    data['realVol'] = list(quote.volume)       
    
    # for json data, numeric type need to be float
    return JsonResponse(data)



def show_exchange(request):
    context_dict = {}
    
    exchange_list = Exchange.objects.all()
    context_dict = {'exchnages': exchange_list}
    
    return render(request, 'riskyNumber/exchange.html', context_dict)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data = request.POST) #, auto_id=True)
        
        user = user_form.save() #save user form data to db
         
        user.set_password(user.password)
        user.save() #update user data
        
        username = request.POST['username'] #return username
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        login(request, user)
            
        return redirect('home')
    else:
        return render(request, 'riskyNumber/registration.html', {'error': 'error message'})
    
def validate_username(request):
    username = request.POST.get('username')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Username: "' + username + '"' + ' already exits. Please select different one.'
    return JsonResponse(data)
 
def authenticate_login(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('uname') #return username
        password = request.POST.get('pword')
        user = authenticate(username = username, password = password)
        
        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('home'))
                data['result'] = 'success'
                return JsonResponse(data)
            else: # make this better
                data['result'] = 'disabled.'
                return JsonResponse(data)
        else:   #elif user == None:
            #print('Invalid login details: {0}, {1}'.format(username, password))
            data['result'] = 'declined'
            return JsonResponse(data)
    data['result'] = 'get'
    return JsonResponse(data)

        
@login_required        
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text!")

def visitor_cookie_handler(request): # for old-> , response):

    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 
                                               'last_visit',
                                               str(dt.now()))
    last_visit_time = dt.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (dt.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(dt.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits
    
def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
    
def search(request):
    result_list = []
    
    if request.method == 'POST':
        query = request.POST['query'].strip()
      
    return render(request, 'riskyNumber/search.html', {'result_list': result_list})
    
def get_ticker_list(max_results = 0, starts_with = ''): # check if list is shorted
    stock_list = []
    if starts_with:
        stock_list = Stock.objects.filter(ticker__istartswith = starts_with)
    if max_results > 0:
        if len(stock_list) > max_results:
            stock_list = stock_list[:max_results]
    return stock_list
    
def suggest_ticker(request):
    stock_list =  []
    starts_with = ''
    
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        #print('suggestion start with:---> ', starts_with)
    stock_list = get_ticker_list(15, starts_with)
    
    # make list of obj to sortable   
    return render(request, 'riskyNumber/ticker.html', {'stocks': stock_list})
   

def get_summary(ticker):
    
    # fundamentals = ['Last', 'Open', '% Changed','Previous Close', 'Changed', 'Volume', 
    #                 'Daily Avg. Volume', 'Year Range', 'Day Range', 'Market Cap', 'EBITDA', 
    #                 'Book Value', '50 DMA', '200 DMA']
    fundamentals = ['Last', 'Open', '% Changed','Previous Close', 'Changed', 'Volume', 
                     'Day Range', 'Year Range']
    tikVals = yf(ticker)
    summary={}
    #if ticker not in ('^DJI', '^IXIC', '^GSPC'):
        # summary['Last'] = str(tikVals.get_price())
        # summary['Open'] = str(tikVals.get_open())
        # summary['% Changed'] = str(tikVals.get_percent_change())
        # summary['Previous Close'] = str(tikVals.get_prev_close())
        # summary['Changed'] = str(tikVals.get_change())
        # summary['Volume'] = str(tikVals.get_volume())
        # summary['Avg. Volume'] = str(tikVals.get_avg_daily_volume())
        # #summary['Day Range'] = str(tikVals.get_days_range())
        # summary['Year Range'] = str(tikVals.get_year_range())
        # fundamentals = fundamentals[:8]
    
    summary['Last'] = str(tikVals.get_price())
    summary['Open'] = str(tikVals.get_open())
    summary['% Changed'] = str(tikVals.get_percent_change())
    summary['Previous Close'] = str(tikVals.get_prev_close())
    summary['Changed'] = str(tikVals.get_change())
    summary['Volume'] = str(tikVals.get_volume())
    #summary['Avg. Volume'] = str(tikVals.get_avg_daily_volume())
    summary['Day Range'] = str(tikVals.get_days_range())
    summary['Year Range'] = str(tikVals.get_year_range())
    #summary['Market Cap'] = str(tikVals.get_market_cap())
    #summary['EBITDA'] = str(tikVals.get_ebitda())
    #summary['Book Value'] = str(tikVals.get_book_value())
    #summary['50 DMA'] = str(tikVals.get_50day_moving_avg())
    #summary['200 DMA'] = str(tikVals.get_200day_moving_avg())
    
    return summary, fundamentals
   



def quote(request): # need this view for pressing enter after ticker input
    data = {}
    ticker = request.GET.get('ticker').upper()
    query = Stock.objects.filter(ticker__iexact=ticker)
    if query:
        data['result'] = 'exist'
        data['ticker'] = ticker
    else:
        data['result'] = 'none' 
    
    return JsonResponse(data) 



@login_required
def register_profile(request):
    form = UserProfileForm()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect('home')
        else:
            print(form.errors)
    context_dict = {'form': form}
    
    return render(request, 'riskyNumber/profile_registration.html', context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return redirect('home')
    userprofile = UserProfile.objects.get_or_create(user = user)[0]
    form = UserProfileForm({'website': userprofile.website,
                            'picture': userprofile.picture})
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
            
    return render(request, 'riskyNumber/profile.html', 
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})
            
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user): 
        
        return reverse('register_profile')
    
def news(ticker):
    rss_reuter = 'http://feeds.reuters.com/reuters/businessNews'
    rss_yahoo = 'http://finance.yahoo.com/rss/headline?s=' + ticker.lower()
    
    newsfeed = feedparser.parse(rss_reuter)
    newsfeed = newsfeed.entries
    
    stockfeed = feedparser.parse(rss_yahoo)
    stockfeed = stockfeed.entries[:12]
    
    newsPosts = []
    stockPosts = []
    
    for post in stockfeed:
        title = post.title
        link = post.link
        stockPosts.append({'title': title, 'link': link})
        
    for post in newsfeed:
        title = post.title
        link = post.link
        newsPosts.append({'title' : title, 'link' : link})
    
    return newsPosts, stockPosts

class fillingThread (Thread):
    def __init__(self, name, ticker):
        Thread.__init__(self)
        self.name = name
        self.ticker = ticker
    def run(self):
        #print("starting thread ***********************")
        data = {}
        cik = tikCikDict[self.ticker]
        data['form'], data['dUrl'], data['des'], data['fDate'] = get_fillings(cik)
        fillingDict[self.ticker] = data
        #print("exiting thread ========================")

def fillings(request):
    data={}
    
    ticker = request.POST.get('ticker').upper()
    # might be better to remove this
    if ticker in fillingDict:
        data = fillingDict[ticker]
        data['result'] = 'gotIt'
    elif ticker in ['^GSPC', '^DJI', '^IXIC']:
        data['result'] = 'invalid'
    else:
        data['result'] = 'gettingIt'
        
    return JsonResponse(data)
    
    
