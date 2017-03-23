from django.contrib import admin
from riskyNumber.models import Exchange, Stock, UserProfile, Trending, Filling
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Exchange)
admin.site.register(Stock)
admin.site.register(UserProfile)
admin.site.register(Trending)
admin.site.register(Filling)
