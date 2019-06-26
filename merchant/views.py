from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from user_auth.models import user_info
from django.contrib.auth import authenticate,login
from user_auth.models import user_info
from django.http import HttpResponse
from .forms import CompanyForm,TruckForm
from .models import Company,TruckInfo
from django.views.decorators.csrf import csrf_exempt
#from customer.models import order,order_bets,items,item_info,order_path_info,items

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


@csrf_exempt
def CompanyRegisterView(request):
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


@csrf_exempt
def TruckRegisterView(request):
    if request.method=='POST':
        truckForm = TruckForm(data=request.POST)
        if truckForm.is_valid():
            t=truckForm.save()
            t.save()
            return redirect("/merchant/")
    else:
        truckForm = TruckForm
    return render(request,'merchant/truck.html',{'truck':truckForm})



def Profile(request):
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


def AllAuctions(request):
    pass