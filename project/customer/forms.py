from django import forms
from django.contrib.auth.models import User
from customer.models import item_info,order_path_info

class ItemInfoForm(forms.ModelForm):
    class Meta():
        model = item_info
        exclude=('order_id','objects','item_id')

class OrderPath(forms.ModelForm):
    class Meta():
        model = order_path_info
        exclude=('order_id','objects')
