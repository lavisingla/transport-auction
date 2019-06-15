from django.shortcuts import render
from .forms import Item_infoForm,OrderForm,Order_path_infoForm,Order_betsForm,Images_by_customerForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
# Create your views here.

def Add_Item_view(request):
    if request.method == 'POST':
        item_infoForm = Item_infoForm(data=request.POST)

        if item_infoForm.is_valid():
            Item_info = item_infoForm.save(commit=False)
            Item_info.save()
            return render(request, 'base.html')
    else:
        item_infoForm = Item_infoForm

    context = {
        'Item_infoForm':item_infoForm,
    }
    return render(request,'customer/additem.html',context)