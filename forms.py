from django import forms
from riskyNumber.models import Stock, UserProfile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class StockForm(forms.ModelForm):
    ticker = forms.CharField(max_length = 10, help_text = 'Enter Page Title')
    
    class Meta:
        model = Stock
        exclude = ('ticker',)
        
class UserForm(forms.ModelForm):
    username = forms.CharField(max_length = 30)
    password = forms.CharField(widget=forms.PasswordInput(), max_length = 30)
                               
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
       
class UserProfileForm(forms.ModelForm):
   
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
    
    
    