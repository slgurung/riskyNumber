from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Exchange(models.Model):
    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name
        
class Stock(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete = models.CASCADE)
    ticker = models.CharField(max_length = 10, primary_key = True)
    cik = models.CharField(max_length = 20, default = '')
    name = models.CharField(max_length = 100, default = '')
    sector = models.CharField(max_length = 100, default = '')
    industry = models.CharField(max_length = 100, default = '')
    
    def __str__(self): # for python 2, use __unicode__ too
        return self.ticker + ': ' + self.name


        
class UserProfile(models.Model):
    # this line is required.
    user = models.OneToOneField(User)
    
    # additional user attributes
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    
    def __str__(self):
        return self.user.username
 
class Trending(models.Model):
    ticker = models.CharField(max_length = 10)
    updown = models.CharField(max_length = 10, blank = True, null = True)    
    
    def __str__(self):
        return self.ticker
    
class Filling(models.Model):
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE)
    form = models.CharField(max_length = 50)
    documentUrl = models.URLField()
    description = models.TextField(null = True)
    fillingDate = models.DateField(null = True)
    
    def __str__(self):
        return self.description




    