from django.contrib import admin
from django.urls import path
from .views import register_view,logout_view

app_name="user_auth"
urlpatterns = [
path('register/',register_view,name='register'),
path('logout/',logout_view,name='logout'),

]
