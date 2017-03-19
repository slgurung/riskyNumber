from django import forms
from riskyNumber.models import Stock, Exchange, UserProfile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class ExchangeForm(forms.ModelForm):
    # A ModelForm maps a model class’s fields to HTML form <input> elements 
    # via a Form; this is what the Django admin is based upo
    name = forms.CharField(max_length = 50, help_text= 'Enter Exchange Name.')
    
    class Meta:
        model = Exchange
        fields = ('name',)
        
class StockForm(forms.ModelForm):
    ticker = forms.CharField(max_length = 10, help_text = 'Enter Page Title')
    #url = forms.URLField(max_length = 200, help_text = 'Enter page URL')
    #views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    '''
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            
            return cleaned_data
    '''
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
    
    
    