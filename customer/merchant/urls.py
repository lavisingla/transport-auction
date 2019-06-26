from django.contrib import admin
from django.urls import path
from merchant import views
from .views import login_view,home_view,CompanyRegisterView,TruckRegisterView,Profile,AllAuctions


app_name="merchant"

urlpatterns = [
path('login/',login_view,name='login'),
path('',home_view,name='home'),
path('addcompany/',CompanyRegisterView,name='addcompany'),
path('addtruck/',TruckRegisterView,name='addtruck'),
path('profile/',Profile,name="profile"),
path('allauctions/',AllAuctions,name="allauctions")
]
