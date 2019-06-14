from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
# Create your views here.

def home_view(request):
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

def login_view(request):
     if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return render(request,'base.html',{})
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

     else:
        #Nothing has been provided for username or password.
        return render(request, 'user_auth/login.html', {})
