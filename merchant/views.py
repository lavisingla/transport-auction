from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from user_auth.models import user_info
from django.contrib.auth import authenticate,login
from user_auth.models import user_info
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CompanyForm,TruckForm,order_betsForm
from .models import Company,TruckInfo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from customer.models import order,order_bets,items,item_info,order_path_info,items
from django.urls import reverse
from merchant.models import permitted_states,Company,TruckInfo,services_provided


#homepage contains all orders related to this merchant
@login_required(login_url='/merchant/login/')
def home_view(request):

    
    #current logged in merchants
    m = request.user
    merchant = user_info.objects.get_merchant_details(merchant_id=m.username)

    ##checking if merchant has registered any truck nd company
    get_companies = Company.objects.get_company_details(merchant[0])
    if not get_companies:
        return redirect("/merchant/addcompany/")

    flg=0
    for c in get_companies:
        trucks = TruckInfo.objects.get_truck_details(c)
        if trucks:
            flg=1
    if flg==0:
        return redirect("/merchant/addtruck/")


    #merchants info
    home_pin =merchant[0].pin_code
    home_state = merchant[0].state
    ratings = merchant[0].ratings
    completed_orders=merchant[0].orders_completed

    orders = order.objects.get_all_requests()
    result= {}
    for o in orders:
        result[o.order_id] = 0
    print(result)

    for o in orders:
        curr_order_path = order_path_info.objects.filter(order_id=o.order_id)
        item_details = item_info.objects.get_item_info(o.order_id)
        order_weight = item_details[0].item_weight
        order_length = item_details[0].item_length
        order_width = item_details[0].item_width
        order_src_city = curr_order_path[0].source_city
        order_src_state=curr_order_path[0].source_state
        order_src_pin=curr_order_path[0].source_pin
        order_dest_city = curr_order_path[0].destination_city
        order_dest_state=curr_order_path[0].destination_state
        order_dest_pin=curr_order_path[0].destination_pin
        customer = user_info.objects.get_user_details(o.customer_id)
        customer_rating = customer[0].ratings

        company = Company.objects.get_company_details(merchant[0])

        for c in company:
            t = TruckInfo.objects.get_truck_details(c)
            flag = 0

            #####checking size of truck and item validation
            for truck in t:
                if truck.Truck_length >= order_length and truck.Truck_capacity >= order_weight and truck.Truck_width >= order_width :
                    flg=1
                    break
                else:
                    continue

            if flg==0:
                continue
            else:
                if not result[o.order_id] > 1:
                    result[o.order_id]=1
                ##checking companies permit validity
                permit_state= permitted_states.objects.get_permitted_states(c.id)
                src=0
                des=0
                for st in permit_state:
                    if st.state == order_src_state:
                        src=1
                    if st.state == order_dest_state:
                        des=1
                if src == 0 or des ==0 :
                    continue
                else:
                    if not result[o.order_id] > 2:
                        result[o.order_id] = 2
                    ##validating services
                    services = services_provided.objects.get_services(c.id)
                    serv=0
                    for ser in services:
                        if ser.id == o.item_id:
                            serv = 1
                    if serv==0:
                        continue
                    else:
                        if not result[o.order_id] > 3:
                            result[o.order_id]=3

                        ##using ratings to give priority
                        if customer_rating > 3 and ratings > 3 :
                            if not result[o.order_id] > 4:
                                result[o.order_id]=4

                        ##checking previous order on same route
                        prev_orders = order.objects.get_previous_orders(merchant[0])
                        for prev in prev_orders:
                            order_path = order_path_info.objects.get_order_path_info(prev.order_id)
                            if order_path[0].source_state == order_src_state:
                                if not result[o.order_id] > 5:
                                    result[o.order_id] = 5
                            if order_path[0].source_ciy == order_src_city:
                                if not result[o.order_id] > 6:
                                    result[o.order_id] = 6

                    ##checking distances

    final_list = []
    final_list = (sorted(result.items(),key = lambda x: (x[1],x[0]),reverse=True))
    return render(request,'merchant/merchant_home.html')

@csrf_exempt
def login_view(request):

     if request.user.is_authenticated:
        return redirect("/merchant/")

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
                # Log the user in.
                user_verification = user_info.objects.check_user(username)
                if user_verification and user_verification[0].merchant==True:
                # Log the user in.
                    login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                    return redirect("/merchant/")
                else:
                    return HttpResponse('Your account exists as user not merchant!!')
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

@login_required(login_url='/merchant/login/')
@csrf_exempt
def CompanyRegisterView(request):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    print(ui.exists())

    if request.method=='POST':
        companyForm = CompanyForm(data=request.POST)
        if companyForm.is_valid():
            company = companyForm.save()
            company.save()
            print(company)
            return redirect("/merchant/")

    else:
        companyForm=CompanyForm
    return render(request,'merchant/company.html',{'company':companyForm})

@login_required(login_url='/merchant/login/')
@csrf_exempt
def TruckRegisterView(request):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    if request.method=='POST':
        truckForm = TruckForm(data=request.POST)
        if truckForm.is_valid():
            t=truckForm.save()
            t.save()
            return redirect("/merchant/")
    else:
        truckForm = TruckForm
    return render(request,'merchant/truck.html',{'truck':truckForm})


@login_required(login_url='/merchant/login/')
def Profile(request):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    current_user = request.user
   # u = user_info.objects.filter(merchant=True)

    c = Company.objects.filter(Owner=ui[0].id)

    t=[]
    for i in c:

        temp = TruckInfo.objects.filter(Company=i.id)
        print(temp.exists())
        if temp.exists()==True:
            print(temp)
            t.append(temp)
        print (t)

    return render(request,'merchant/profile.html',{'u':ui,'c':c,'t':t})

@login_required(login_url='/merchant/login/')
def AllAuctions(request):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    order_bet = order_bets.objects.all()
    orders = order.objects.all()
    order_path_infos = order_path_info.objects.all()
    item_infos = item_info.objects.all()
    ongoing_path_list=[]
    item_info_list=[]
    for  i in orders:
        o=order_path_info.objects.get_order_path_info(i.order_id)
        ongoing_path_list.append([o[0].order_id,o[0].source_city,o[0].source_state,o[0].destination_city,o[0].destination_state])
        i=item_info.objects.get_item_info(i.order_id)
        item_info_list.append([i[0].order_id,i[0].item_weight,i[0].item_length,i[0].item_width,i[0].item_height])
        curr_bet = order_bets.objects.filter(order_id=i)

    #print(order[0].extra_info)
    return render(request,'merchant/allauctions.html',{'orders':orders,'order_bet':order_bet,'order_path_infos':ongoing_path_list,'item_infos': item_info_list})
@login_required(login_url='/merchant/login/')
def bets_view(request,order_id):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    order_bet = order_bets.objects.get_bets(order_id)
    return render(request,'merchant/bets.html',{'order_bet':order_bet,'order_id':order_id})


@login_required(login_url='/merchant/login/')
def make_bet_view(request,order_id):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    # obj = get_object_or_404(order_bets, order_id = order_id)
    merchant_name = request.user
    o = order_id
    merchant = user_info.objects.filter(user=merchant_name)
    print(merchant[0])
    if request.method == 'POST':
        make_bet = order_betsForm(data=request.POST)
        print(make_bet.is_valid())
        if make_bet.is_valid():
            bet = make_bet.save(commit=False)
            bet.order_id = order_id
            bet.merchant_id = merchant[0]
            bet.save()
            return redirect('/merchant/allauctions')
    else:
         make_bet = order_betsForm


    return render(request,'merchant/make_bet.html',{'make_bet':make_bet})
