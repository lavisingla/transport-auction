from django.contrib import admin
from django.urls import path
from .views import login_view,ongoing_orders_view,previous_orders_view,pending_requests_view,home_view
from .views import merchant_detail_view,bets_view,profile_view,placeRequest_view

app_name="customer"

urlpatterns = [
path('login/',login_view,name='login'),
path('',home_view,name='home'),
path('ongoing_orders/',ongoing_orders_view,name='ongoing_orders'),
path('previous_orders/',previous_orders_view,name='previous_orders'),
path('pending_requests/',pending_requests_view,name='pending_requests'),
path('merchant_detail/<slug:merchant_id>/',merchant_detail_view,name="merchant_details"),
path('bets/<slug:order_id>/',bets_view,name="bets_detail"),
path('profile',profile_view,name="profile"),
path('place-request/<int:itemId>/',placeRequest_view,name="place_request"),
]
