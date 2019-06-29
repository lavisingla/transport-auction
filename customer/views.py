from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from user_auth.models import user_info
from .models import order,order_bets,items,item_info,order_path_info,items
from .forms import ItemInfoForm,OrderPath,OrderForm
from datetime import datetime,date
from .tasks import comfirm_order
from django.contrib.auth.decorators import login_required
a = 12

@login_required(login_url='/customer/login/')
def home_view(request):
    item = items.objects.all()
    return render(request,'customer/customer_home.html',{'items':item})

def login_view(request):

         if request.user.is_authenticated:
            return redirect("/customer/")

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
                    print(user_verification[0].merchant)
                    if user_verification and user_verification[0].merchant==False:
                    # Log the user in.
                        login(request,user)
                    # Send the user back to some page.
                    # In this case their homepage.
                        return redirect("/customer/")
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

@login_required(login_url='/customer/login/')
def ongoing_orders_view(request):
    user = request.user
    ui = user_info.objects.filter(user=user) 
    username = user.username
    ongoing_orders = order.objects.get_orders_ongoing(ui[0])
    ongoing_path_list=[]
    item_info_list=[]
    for orders in ongoing_orders:
        o=order_path_info.objects.get_order_path_info(orders.order_id)
        ongoing_path_list.append([o[0].order_id,o[0].source_city,o[0].source_state,o[0].destination_city,o[0].destination_state])
        i=item_info.objects.get_item_info(orders.order_id)
        item_info_list.append([i[0].order_id,i[0].item_weight,i[0].item_length,i[0].item_width,i[0].item_height])

    context={'ongoing_orders':ongoing_orders
            ,'ongoing_path_list':ongoing_path_list,
            'item_info_list':item_info_list}
    return render(request,'customer/ongoing_orders.html',context)

@login_required(login_url='/customer/login/')
def previous_orders_view(request):
    u= request.user
    print(u)
    ui = user_info.objects.filter(user=u)
    print(ui[0])
    
    previous_orders = order.objects.get_previous_orders(ui[0])
    print(previous_orders)
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
@login_required(login_url='/customer/login/')
def pending_requests_view(request):
    user = request.user
    u = user_info.objects.filter(user=user)
    username = user.username
    to = datetime.now()
    t = str(to)
    req = t[0:4]+t[5:7]+t[8:10]+t[11:13]+t[14:16]+t[17:19]+t[20:26]
    print(req)
    pending_orders = order.objects.get_pending_requests(u[0])
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

@login_required(login_url='/customer/login/')
def merchant_detail_view(request,merchant_id):
    merchant = user_info.objects.get_merchant_details(merchant_id=merchant_id)
    return render(request,'customer/merchant_detail.html',{'merchant':merchant[0],})

@login_required(login_url='/customer/login/')
def bets_view(request,order_id):
    bets = order_bets.objects.get_bets(order_id)
    return render(request,'customer/bets.html',{'bets':bets})

@login_required(login_url='/customer/login/')
def profile_view(request):
    user = request.user
    user_inform=user_info.objects.get_user_details(user.username)
    return render(request,'customer/profile.html',{'user':user,'user_info':user_inform[0]})

@login_required(login_url='/customer/login/')
def placeRequest_view(request,itemId):
    user = request.user
    if request.method =='POST':
        item_info = ItemInfoForm(data=request.POST)
        path = OrderPath(data=request.POST)
        ord=OrderForm(data=request.POST)

        if item_info.is_valid and path.is_valid:
            to = datetime.now()
            t = str(to)
            req = t[0:4]+t[5:7]+t[8:10]+t[11:13]+t[14:16]+t[17:19]+t[20:26]
            order_path = path.save(commit=False)
            order_path.order_id = req
            item = item_info.save(commit=False)
            item.order_id=req
            item.item_id=itemId
            cust = user_info.objects.filter(user=user)
            order_new = order(order_id=req,item_id=itemId,customer_id=cust[0])
            order_new.save()
            item.save()
            order_path.save()

            comfirm_order(req)
            return redirect('/customer/')

    else:
        item_info=ItemInfoForm
        path=OrderPath
        ord=OrderForm

    context={
    'item_info_form':item_info,
    'path_form':path,
    'order':ord
    }
    return render(request,'customer/addrequest.html',context)

