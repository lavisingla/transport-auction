from django.contrib import admin
from django.urls import path
from .views import login_view,ongoing_orders_view,previous_orders_view,pending_requests_view
from .views import merchant_detai_view

app_name="customer"

urlpatterns = [
path('login/',login_view,name='login'),
path('ongoing_orders/',ongoing_orders_view,name='ongoing_orders'),
path('previous_orders/',previous_orders_view,name='previous_orders'),
path('pending_requests/',pending_requests_view,name='pending_requests'),
path('merchant_detail/<slug:merchant_id>/',merchant_detai_view,name="merchant_details")
]
