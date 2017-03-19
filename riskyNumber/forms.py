from django import forms
from riskyNumber.models import Stock, Exchange, UserProfile
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
                               #validators=[RegexValidator(r'^[\w]+$', message='5-30 long', code='invalid password' ),],
                               #help_text= "<= 30 characters.Alphanumeric, _,@, ., +, - only")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
        #widgets = {'password': forms.TextInput(attrs= {'size': 40})}
        '''
        labels ={
                'email': _('Emails '),
                'first_name': _('First Name'),
                'last_name': _('Last Name'), 
                }
        '''
        
class UserProfileForm(forms.ModelForm):
    #website = forms.URLField(required = False)
    #picture = forms.ImageField(required = False)
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
    
    
    