from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from user_auth.models import user_info

def login_view(request):

         if request.user.is_authenticated:
            return render(request,'base2.html',{})

         if request.method == 'POST':
            # First get the username and password supplied
            username = request.POST.get('username')
            password = request.POST.get('password')
            print("They used username: {} and password: {}".format(username,password))

            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)

            # If we have a user
            if user:

                #Check it the account is active
                if user.is_active:
                    user_verification = user_info.objects.check_user(username)
                    if user_verification and user_verification[0].merchantOrUser=='user':
                    # Log the user in.
                        login(request,user)
                    # Send the user back to some page.
                    # In this case their homepage.
                        return render(request,'base2.html',{})
                    else:
                        return HttpResponse('Your account exists as merchant not user!!')

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
