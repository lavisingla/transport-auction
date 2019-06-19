from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from user_auth.models import user_info
from .models import order,order_bets,items,item_info,order_path_info,items


def home_view(request):
    item = items.objects.all()
    return render(request,'customer/customer_home.html',{'items':item})

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
    ongoing_orders = order.objects.get_orders_ongoing(username)
    ongoing_path_list=[]
    item_info_list=[]
    for orders in ongoing_orders:
        o=order_path_info.objects.get_order_path_info(orders.order_id)
        ongoing_path_list.append([o[0].order_id,o[0].source_city,o[0].source_state,o[0].destination_city,o[0].destination_state])
        i=item_info.objects.get_item_info(orders.order_id)
        item_info_list.append([i[0].order_id,i[0].item_weight,i[0].item_length,i[0].item_width,i[0].item_height])

    print(ongoing_path_list[0])
    context={'ongoing_orders':ongoing_orders
            ,'ongoing_path_list':ongoing_path_list,
            'item_info_list':item_info_list}
    return render(request,'customer/ongoing_orders.html',context)


def previous_orders_view(request):
    user = request.user
    username = user.username
    previous_orders = order.objects.get_previous_orders(username)
    previous_path_list=[]
    item_info_list=[]
    for orders in previous_orders:
        o=order_path_info.objects.get_order_path_info(orders.order_id)
        previous_path_list.append([o[0].order_id,o[0].source_city,o[0].source_state,o[0].destination_city,o[0].destination_state])
        i=item_info.objects.get_item_info(orders.order_id)
        item_info_list.append([i[0].order_id,i[0].item_weight,i[0].item_length,i[0].item_width,i[0].item_height])

    context={'previous_orders':previous_orders
            ,'previous_path_list':previous_path_list,
            'item_info_list':item_info_list}
    return render(request,'customer/previous_orders.html',context)

def pending_requests_view(request):
    user = request.user
    username = user.username
    print(username)
    pending_orders = order.objects.get_pending_requests(username)
    pending_path_list=[]
    item_info_list=[]
    for orders in pending_orders:
        o=order_path_info.objects.get_order_path_info(orders.order_id)
        pending_path_list.append([o[0].order_id,o[0].source_city,o[0].source_state,o[0].destination_city,o[0].destination_state])
        i=item_info.objects.get_item_info(orders.order_id)
        item_info_list.append([i[0].order_id,i[0].item_weight,i[0].item_length,i[0].item_width,i[0].item_height])

    context={'pending_orders':pending_orders
            ,'pending_path_list':pending_path_list,
            'item_info_list':item_info_list}
    return render(request,'customer/pending_requests.html',context)

def merchant_detail_view(request,merchant_id):
    merchant = user_info.objects.get_merchant_details(merchant_id=merchant_id)
    return render(request,'customer/merchant_detail.html',{'merchant':merchant[0],})

def bets_view(request,order_id):
    bets = order_bets.objects.get_bets(order_id)
    return render(request,'customer/bets.html',{'bets':bets})

def profile_view(request):
    user = request.user;
    user_inform=user_info.objects.get_user_details(user.username)
    return render(request,'customer/profile.html',{'user':user,'user_info':user_inform[0]})
