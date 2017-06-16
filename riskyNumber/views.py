#######################
from threading import Thread
from math import pi
import pandas as pd
import numpy as np
from pandas_datareader import data as web
import feedparser
from datetime import datetime as dt
from datetime import date, timedelta
from yahoo_finance import Share as yf

#from bokeh.plotting import figure
#from bokeh.io import save, output_file, show
#from bokeh.embed import components
#from bokeh.resources import CDN
#from bokeh.models import *

#####################################

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from riskyNumber.intradayData import get_intraday
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



tikCikDict = {}
if not tikCikDict:
    tikCikDf = pd.read_csv('tickerCik.txt', index_col = 0, na_values = ['', 'NaN'], dtype = {'CIK': str})
    tikCikDict = dict(zip(list(tikCikDf.Symbol), list(tikCikDf.CIK)))
    #print('seting CIK dictionary **************************')

fillingDict={}

####### do something for begining setup
trendList = []

Trending.objects.all().delete()
trendList = get_trending()
for t in trendList:
    trendStk = Trending(ticker = t)
    trendStk.save()

stkIndex = {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones Industrial' , '^IXIC': 'Nasdaq Composite'}
        
def about(request):
    
    context_dict = {}
    context_dict['trending'] = trendList
    
    
    return render(request, 'riskyNumber/about.html', context_dict)

def index(request):
    context_dict = {}
    
    context_dict['trending'] = trendList
    ticker = '^GSPC' #trendList[0]
    context_dict['ticker'] = ticker    
    context_dict['name'] = 'S&P 500'
    ##########################################################        
    #if ticker not in fillingDict:
    #    fThread = fillingThread('filling:' + ticker, ticker)
    #    fThread.start()
    ##########################################################
    #trend = []
    #for symbol in trending:
    #    tikVals = yf(symbol)
    #    if (float(tikVals.get_percent_change().split('%')[0]) > 0):
    #        trend.append("green")
    #    else:
    #        trend.append("red")
    #context_dict['trend'] = trend  
    
    #request.session.set_test_cookie()
    #exchange_list = Exchange.objects.all()
    #page_list = Page.objects.order_by('-views')[:5]
    #context_dict = {'exchanges': exchange_list}
    # obtain response obj before return to add cookie
    #response = render(request, 'rango/index.html', context_dict)
    #visitor_cookie_handler(request, response)
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    context_dict['summary'], context_dict['fundamentals'] = get_summary(ticker)   
    
    quote = get_intraday(ticker)    #[0:50]
    quote = quote.applymap(lambda x: pd.to_numeric(x))

    dateSeries = quote.date.map(lambda x: dt.fromtimestamp(x))
    #context_dict['date'] = list(quote.date)
    #startDate = dt.fromtimestamp(quote.date[0])
    #startDate = startDate.date().strftime("%Y-%m-%d")
    #startDate = dateSeries[0].date().strftime("%Y-%m-%d")
    #i = quote.index #range(len(quote)))
    context_dict['date'] = list(dateSeries.map(str)) # change Timestamp obj to string. but don't work strftime()
    #startDate = context_dict['date'][0].split(' ')[0]
    startDate = str(dateSeries[0].date())
    
    context_dict['start'] = startDate + ' 9:30:00'
    context_dict['end'] = startDate + ' 16:00:00'
       
    context_dict['close'] = list(quote['close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    #context_dict['vol'] = quote.volume
    
    context_dict['min'] = min(context_dict['low'])
    context_dict['max'] = max(context_dict['high'])  
    
    context_dict['businessNews'], context_dict['stockNews'] = news(ticker) # save this for quick download
   
    return render(request, 'riskyNumber/index.html', context_dict)
    
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
    
    fundamentals = ['Last', 'Open', '% Changed','Previous Close', 'Changed', 'Volume', 
                    'Daily Avg. Volume', 'Year Range', 'Day Range', 'Market Cap', 'EBITDA', 
                    'Book Value', '50 DMA', '200 DMA']
    tikVals = yf(ticker)
    summary={}
    if(ticker == '^DJI' or ticker == '^IXIC' or ticker == '^GSPC'):
        summary['Last'] = str(tikVals.get_price())
        summary['Open'] = str(tikVals.get_open())
        summary['% Changed'] = str(tikVals.get_percent_change())
        summary['Previous Close'] = str(tikVals.get_prev_close())
        summary['Changed'] = str(tikVals.get_change())
        summary['Volume'] = str(tikVals.get_volume())
        summary['Avg. Volume'] = str(tikVals.get_avg_daily_volume())
        #summary['Day Range'] = str(tikVals.get_days_range())
        summary['Year Range'] = str(tikVals.get_year_range())
        fundamentals = fundamentals[:8]
    else:
        summary['Last'] = str(tikVals.get_price())
        summary['Open'] = str(tikVals.get_open())
        summary['% Changed'] = str(tikVals.get_percent_change())
        summary['Previous Close'] = str(tikVals.get_prev_close())
        summary['Changed'] = str(tikVals.get_change())
        summary['Volume'] = str(tikVals.get_volume())
        summary['Avg. Volume'] = str(tikVals.get_avg_daily_volume())
        summary['Day Range'] = str(tikVals.get_days_range())
        summary['Year Range'] = str(tikVals.get_year_range())
        summary['Market Cap'] = str(tikVals.get_market_cap())
        summary['EBITDA'] = str(tikVals.get_ebitda())
        summary['Book Value'] = str(tikVals.get_book_value())
        summary['50 DMA'] = str(tikVals.get_50day_moving_avg())
        summary['200 DMA'] = str(tikVals.get_200day_moving_avg())
    
    return summary, fundamentals
   
def summary(request, ticker):
    context_dict = {}
    context_dict['ticker'] = ticker
    if ticker not in ['^GSPC', '^DJI', '^IXIC']:
        stkObj = Stock.objects.get(ticker = ticker).name.split(" ")[:2]
        if len(stkObj) > 1:
            context_dict['name'] = stkObj[0] + " " +stkObj[1]
        else:
            context_dict['name'] = stkObj[0]
    else:
        context_dict['name'] = stkIndex[ticker]
        
    
    if ticker not in ['^GSPC', '^DJI', '^IXIC'] and ticker not in fillingDict:
        fThread = fillingThread('filling:' + ticker, ticker)
        fThread.start()
    
    trending = Trending.objects.all()
    trending = [trend.ticker for trend in trending]
    context_dict['trending'] = trending
          
    context_dict['summary'], context_dict['fundamentals'] = get_summary(ticker)   
    
    quote = get_intraday(ticker)
    quote = quote.applymap(lambda x: pd.to_numeric(x))
    
    dateSeries = quote.date.map(lambda x: dt.fromtimestamp(x))
    #context_dict['date'] = list(quote.date)
    #startDate = dt.fromtimestamp(quote.date[0])
    #startDate = startDate.date().strftime("%Y-%m-%d")
    #startDate = context_dict['date'][0].date().strftime("%Y-%m-%d")
    #context_dict['date'] = list(dateSeries.strftime("%Y-%m-%d %H:%M:%S"))
    context_dict['date'] = list(dateSeries.map(str)) # change Timestamp obj to string. but don't work strftime()
    startDate = context_dict['date'][0].split(' ')[0]
    
    context_dict['start'] = startDate + ' 9:30:00'
    context_dict['end'] = startDate + ' 16:00:00'
        
    context_dict['close'] = list(quote['close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    #context_dict['vol'] = pd.to_numeric(quote.volume)
   
    context_dict['min'] = min(context_dict['low'])
    context_dict['max'] = max(context_dict['high'])  
        
    context_dict['businessNews'], context_dict['stockNews'] = news(ticker) # save this for quick download
       
    return render(request, 'riskyNumber/summary.html', context_dict)

# not using now?    
def intradayValues(ticker):
    context_dict = {}
    quote = get_intraday(ticker)
    quote = quote.applymap(lambda x: pd.to_numeric(x))
    i = quote.index #range(len(quote)))
    i = list(i.strftime("%Y-%m-%d %H:%M:%S"))
    
    startDate = i[0].split(' ')[0]
    context_dict['start'] = startDate + ' 9:30:00'
    context_dict['end'] = startDate + ' 16:00:00'
    #context_dict['today'] = i[0].split(' ')[0]
    context_dict['date'] = i
    context_dict['close'] = list(quote['close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    #context_dict['vol'] = pd.to_numeric(quote.volume)
   
    context_dict['min'] = min(context_dict['low'])
    context_dict['max'] = max(context_dict['high'])  
    
    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    y = min(context_dict['high']) 
    x = context_dict['min'] 
    
    context_dict['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)    
    context_dict['volMin'] = min(context_dict['vol'])
    context_dict['volMax']= max(context_dict['vol'])
    return context_dict

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

# not using it????  
def update_chart(request): #for ajax
    end = date.today()
    start = end - timedelta(365/12)
    if request.method == 'GET':
        ticker = request.GET['ticker']
    quote = web.DataReader(ticker, 'yahoo', start, end)
    context_dict = {}
    
    i = quote.index #range(len(quote)))
    i = list(i.strftime("%b%d"))
        
    
    context_dict['date'] = i
    context_dict['close'] = list(quote['Close'])
    context_dict['open'] = list(quote.Open)
    context_dict['high'] = list(quote.High)
    context_dict['low'] = list(quote.Low)
    
    context_dict['min'] =  quote.Low.min()
    context_dict['max'] =  quote.High.max()  
    #context_dict['vol'] = list(quote.Volume)
    maxVol = quote.Volume.max()
    minVol = quote.Volume.min()
    y = quote.High.min() * 1.01
    x = context_dict['min']
    #context_dict['vol'] = list(quote.Volume)
    context_dict['vol'] = list(((quote.Volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  

    return render(request,'riskyNumber/updateChart.html' , context_dict)

# not using it??   
def chart(request, tkperiod): 
    context_dict = {}
    end = date.today()
    chartperiod = tkperiod[-2:]
    ticker = tkperiod[:-2]
    
    if(chartperiod == 'd5'):
        start = end - timedelta(5) 
    elif(chartperiod == 'm1'):  
        start = end - timedelta(365/12)        
    elif(chartperiod == 'm6'):
        start = end - timedelta(365/2)
    elif(chartperiod == 'y1'): 
        start = end - timedelta(365)
    elif(chartperiod == 'y2'): 
        start = end - timedelta(730)
    elif(chartperiod == 'y5'): 
        start = end - timedelta(1825)
    else:
        return redirect ('summary', ticker=ticker) #summary(request, ticker)
    
    if(chartperiod != 'd5'):
        quote = web.DataReader(ticker, 'yahoo', start, end)
        quote.columns = map(str.lower, quote.columns)
        i = quote.index #range(len(quote)))
        i = list(i.strftime("%b %d '%y"))
    else:
        quote = get_intraday(ticker, 5)
        quote = quote.applymap(lambda x: pd.to_numeric(x))
        i = quote.index #range(len(quote)))
        #i = list(i.strftime("%I:%M %p, %a"))
        i = list(i.strftime("%Y-%m-%d %H:%M:%S"))
    
    context_dict['ticker'] = ticker
    trending = Trending.objects.all()
    trending = [trend.ticker for trend in trending]
    context_dict['trending'] = trending
    
    context_dict['date'] = i
    context_dict['close'] = list(quote['close'])
    context_dict['open'] = list(quote.open)
    context_dict['high'] = list(quote.high)
    context_dict['low'] = list(quote.low)
    context_dict['min'] =  quote.low.min()
    context_dict['max'] =  quote.high.max()  
    
    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    y = quote.high.min() 
    x = context_dict['min']
    
    context_dict['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  
    context_dict['volMin'] = min(context_dict['vol'])
    context_dict['volMax']= max(context_dict['vol'])
    context_dict['businessNews'], context_dict['stockNews'] = news(ticker) # save this for quick download
    
    return render(request,'riskyNumber/chart.html', context_dict)
       
def hChart(request):
    data = {}
    chartPeriod = request.POST.get('chartPeriod')
    ticker = request.POST.get('ticker')
    
    end = date.today()
    
    if(chartPeriod == 'd5'):
        quote = get_intraday(ticker, 5)
        data['dateVal'] = list(quote.date) # need to be before below change to numeric
        # because numeric values couldn't be json serializable
        quote = quote.applymap(lambda x: pd.to_numeric(x))
        
        
        #i = quote.index #range(len(quote)))
        #i = list(i.strftime("%Y-%m-%d %H:%M:%S"))
    elif(chartPeriod == 'm1'):  
        start = end - timedelta(365/12)        
    elif(chartPeriod == 'm6'):
        start = end - timedelta(365/2)
    elif(chartPeriod == 'y1'): 
        start = end - timedelta(365)
    elif(chartPeriod == 'y2'): 
        start = end - timedelta(730)
    elif(chartPeriod == 'y5'): 
        start = end - timedelta(1825)
    elif(chartPeriod == 'd1'):
        #quote = get_intraday(ticker)
        #quote = quote.applymap(lambda x: pd.to_numeric(x))
        quote = get_intraday(ticker)
        data['dateVal'] = list(quote.date)
        quote = quote.applymap(lambda x: pd.to_numeric(x))

        startDate = dt.fromtimestamp(quote.date[0])
        startDate = startDate.date().strftime("%Y-%m-%d")
    
        data['start'] = startDate + ' 9:30:00'
        data['end'] = startDate + ' 16:00:00'
        
        #i = quote.index #range(len(quote)))
        #i = list(i.strftime("%Y-%m-%d %H:%M:%S"))
        #startDate = i[0].split(' ')[0]
        #data['start'] = startDate + ' 9:30:00'
        #data['end'] = startDate + ' 16:00:00'
        
    if chartPeriod not in ['d5', 'd1']:
        # this df has index as datetime object
        quote = web.DataReader(ticker, 'yahoo', start, end)
        quote.columns = map(str.lower, quote.columns)
        i = quote.index #range(len(quote)))
        #i = list(i.strftime("%b %d '%y")) # This doesn't work in javascript end for ubuntu
        i = list(i.strftime("%Y-%m-%d"))
        data['dateVal'] = i
        
    data['ticker'] = ticker
    data['close'] = list(quote['close'])
    data['open'] = list(quote.open)
    data['high'] = list(quote.high)
    data['low'] = list(quote.low)
    data['min'] =  quote.low.min()
    data['max'] =  quote.high.max()  
    
    maxVol = quote.volume.max()
    minVol = quote.volume.min()
    y = quote.high.min() 
    x = data['min']
   
    data['vol'] = list(((quote.volume - minVol) * ((y-x)/(maxVol - minVol))) + x)  
    data['volMin'] = min(data['vol'])
    data['volMax']= max(data['vol'])    
        
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
    
    
