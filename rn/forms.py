from django import forms
from rn.models import UserDetails,UserProfile
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=UserDetails
        
    
    
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=40,widget=forms.PasswordInput())
   

