from django.contrib import admin
from django.urls import path
from merchant import views
from .views import login_view


app_name="merchant"

urlpatterns = [
path('login/',login_view,name='login'),
]
