"""riskyNumberProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from riskyNumber import views
from django.conf import settings
from django.conf.urls.static import static

'''
urlpatterns = [
    url(r'^$', views.index, name = 'home'),
    url(r'^riskyNumber/', include('riskyNumber.urls')),
    url(r'^shouelkwhods/', admin.site.urls),
    #url(r'^accounts/register/$', views.MyRegistrationView.as_view(),
    #               name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # PAGE 41
'''
urlpatterns = [ url(r'^$', views.index, name = 'home'), # rango/
		           url(r'^admin/', admin.site.urls),
               url(r'^about/$', views.about, name = 'about'),
               url(r'^show_exchange/$', views.show_exchange, name = 'show_exchange'),
               url(r'search/$', views.search, name = 'search'),
               url(r'^suggest/$', views.suggest_ticker, name = 'suggest_ticker'),
               url(r'^summary/(?P<ticker>[\^\w]+)/$', views.summary, 
                                   name = 'summary'),
               url(r'^quote/$', views.quote, name = 'quote'),
               #url(r'^updateChart/$', views.update_chart, name= 'update_chart'),
               url(r'^hChart/$', views.hChart, name='historical_chart'),
               #url(r'^chart/(?P<tkperiod>[\.\w]+)/$', views.chart, name= 'chart'),   
               url(r'^register/$', views.register, name = 'register'),
               url(r'^validate_username/$', views.validate_username, name = 'validate_username'),
               url(r'^authenticate_login/$', views.authenticate_login, name = 'authenticate_login'),
               #url(r'^login/$', views.user_login, name = 'login'),
               url(r'^register_profile/$', views.register_profile, name='register_profile'),
               url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name = 'profile'),
               url(r'^fillings/$', views.fillings, name = 'fillings'),
		           url(r'^accounts/', include('registration.backends.simple.urls')),
            ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # PAGE 41

