from django.contrib import admin
from django.urls import path
from .views import Add_Item_view


app_name="customer"
urlpatterns = [
    path('additem/',Add_Item_view,name='additem'),


]