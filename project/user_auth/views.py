from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth import logout

# Create your views here.

def home_view(request):
    if not request.user.is_authenticated:
        return render(request,'base.html',{})
    return render(request,'base2.html',{})


def logout_view(request):
    logout(request)
    return render(request,'base.html',{})


def register_view(request):
    registered=False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm
        profile_form=UserProfileInfoForm

    context={
    'user_form':user_form,
    'profile_form':profile_form,
    'registered':registered,
    }
    return render(request,'user_auth/register.html',context)
