from django.contrib import admin
from django.urls import path
from merchant import views
from .views import make_bet_view,login_view,home_view,CompanyRegisterView,TruckRegisterView,Profile,AllAuctions,bets_view


app_name="merchant"

urlpatterns = [
path('login/',login_view,name='login'),
path('',home_view,name='home'),
path('addcompany/',CompanyRegisterView,name='addcompany'),
path('addtruck/',TruckRegisterView,name='addtruck'),
path('profile/',Profile,name="profile"),
path('allauctions/',AllAuctions,name="allauctions"),
path('bets/<slug:order_id>/',bets_view,name="bets_detail"),
path('makebets/<slug:order_id>/',make_bet_view,name="make_bet"),
]
