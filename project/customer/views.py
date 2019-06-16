from django.shortcuts import render
from .forms import Item_infoForm,OrderForm,Order_path_infoForm,Order_betsForm,Images_by_customerForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
# Create your views here.

def Add_Item_view(request):
    if request.method == 'POST':
        item_infoForm = Item_infoForm(data=request.POST)

        if item_infoForm.is_valid():
            Item_info = item_infoForm.save(commit=False)
            Item_info.save()
            return render(request, 'base.html')
    else:
        item_infoForm = Item_infoForm

    context = {
        'Item_infoForm':item_infoForm,
    }
    return render(request,'customer/additem.html',context)
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from user_auth.models import user_info
from .models import order,order_bets,items,item_info,order_path_info

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

def ongoing_orders_view(request):
    user = request.user
    username = user.username

    print(username)
    ongoing_orders = order.objects.get_orders_ongoing(username)
    for i in ongoing_orders:
        print(i.order_id)
        print(i.customer_id)
    return HttpResponse('good work')


def previous_orders_view(request):
    user = request.user
    username = user.username

    previous_orders = order.objects.get_previous_orders(username)

    for i in previous_orders:
        print(i.order_id)
        print(i.customer_id)
    return HttpResponse('good work')

def pending_requests_view(request):
    user = request.user
    username = user.username

    pending_requests = order.objects.get_pending_requests(username)
    for i in pending_requests:
        print(i.order_id)
        print(i.customer_id)
    return HttpResponse('good work')
