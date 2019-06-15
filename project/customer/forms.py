from django import forms
from django.contrib.auth.models import User
from .models import order,order_bets,order_path_info,item_info,images_by_customer
from user_auth.models import user_info


class Item_infoForm(forms.ModelForm):
    class Meta():
        model=item_info
        fields=('item_name','item_weight','item_length','item_width','item_height','handle_with_care','item_material','item_approximate_cost')


class OrderForm(forms.ModelForm):
    class Meta():
        model = order
        fields=('item_id','customer','merchant','comfirmed')

class Order_path_infoForm(forms.ModelForm):
    class Meta():
        model = order_path_info
        fields = ('order_id','source_area','source_city','source_state','source_pin','destination_area','destination_city','destination_state','destination_pin')

class Order_betsForm(forms.ModelForm):
    class Meta():
        model = order_bets
        fields = ('order_id','merchant_id','bet_price','extra_info','pickup_days')

class Images_by_customerForm(forms.ModelForm):
    class Meta():
        model = images_by_customer
        fields = ('item_information','image')