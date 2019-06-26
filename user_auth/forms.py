from django import forms
from django.contrib.auth.models import User
from .models import user_info

#user basic details like password and username
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')

#extra details of user
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = user_info
        fields=('contact','area','city','pin_code','state','merchant')
