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
def home_view(request):
    
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
    u = user_info.objects.filter(merchant=True)

    c = Company.objects.filter(Owner=u[0].id)
    
    t=[]
    for i in c:
        
        temp = TruckInfo.objects.filter(Company=i.id)
        print(temp.exists())
        if temp.exists()==True:
            print(temp)
            t.append(temp)
        print (t)
    
    return render(request,'merchant/profile.html',{'u':u,'c':c,'t':t})

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
    for  i in orders:
        print("The order is ")
        print(i)
        print("\n")
        curr_bet = order_bets.objects.filter(order_id=i)
        print("current bet is")
        print(curr_bet)
    #print(order[0].extra_info)
    return render(request,'merchant/allauctions.html',{'orders':orders,'order_bet':order_bet,'order_path_infos':order_path_infos,'item_infos': item_infos})
@login_required(login_url='/merchant/login/')
def bets_view(request,order_id):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    order_bet = order_bets.objects.get_bets(order_id)
    return render(request,'merchant/bets.html',{'order_bet':order_bet})


@login_required(login_url='/merchant/login/')
def make_bet_view(request,order_id):
    u = request.user
    ui = user_info.objects.filter(user=u,merchant=True)
    if ui.exists()==False:
        return render(request,'merchant/wronguser.html')
    obj = get_object_or_404(order_bets, order_id = order_id)
    merchant_name = request.user
    o = order_id
    merchant = user_info.objects.filter(user=merchant_name)
    print(merchant[0])
    if request.method == 'POST':
        make_bet = order_betsForm(data=request.POST,instance=obj,merchant_id = merchant[0],order_id = o)

        #make_bet.order_id = order_id
        #make_bet.merchant_id = merchant
        print(make_bet.is_valid())
        if make_bet.is_valid():
            make_bet.order_id = order_id
            make_bet.merchant_id = merchant[0]
            make_bet.save(commit=True)
            return redirect('/merchant/allauctions')
    else:
         make_bet = order_betsForm


    return render(request,'merchant/make_bet.html',{'make_bet':make_bet})