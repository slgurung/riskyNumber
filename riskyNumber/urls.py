from django.conf.urls import url
from riskyNumber import views

urlpatterns = [ url(r'^$', views.index, name = 'home'), # rango/
               url(r'^about/$', views.about, name = 'about'),
               url(r'^show_exchange/$', views.show_exchange, name = 'show_exchange'),
               url(r'search/$', views.search, name = 'search'),
               url(r'^suggest/$', views.suggest_ticker, name = 'suggest_ticker'),
<<<<<<< HEAD
               url(r'^summary/(?P<ticker>[\^\w]+)/$', views.summary, 
=======
               url(r'^summary/(?P<ticker>[\.\w]+)/$', views.summary, 
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
                                   name = 'summary'),
               url(r'^quote/$', views.quote, name = 'quote'),
               url(r'^updateChart/$', views.update_chart, name= 'update_chart'),
               url(r'^hChart/$', views.hChart, name='historical_chart'),
<<<<<<< HEAD
               url(r'^chart/(?P<tkperiod>[\^\w]+)/$', views.chart, name= 'chart'),   
=======
               #url(r'^chart/(?P<tkperiod>[\.\w]+)/$', views.chart, name= 'chart'),   
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
               url(r'^register/$', views.register, name = 'register'),
               url(r'^validate_username/$', views.validate_username, name = 'validate_username'),
               url(r'^authenticate_login/$', views.authenticate_login, name = 'authenticate_login'),
               #url(r'^login/$', views.user_login, name = 'login'),
               url(r'^register_profile/$', views.register_profile, name='register_profile'),
               url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name = 'profile'),
               url(r'^fillings/$', views.fillings, name = 'fillings'),
            ]
            