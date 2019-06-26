from background_task import background
from django.contrib.auth.models import User
from .models import items,order,order_bets
from django.shortcuts import get_object_or_404




@background(schedule=300)
def comfirm_order(order_id):
    print('lavi')
    bets = order_bets.objects.get_bets(order_id=order_id)
    ord = get_object_or_404(order,order_id=order_id)
    ord.merchant_id=bets[0].merchant_id
    ord.comfirmed=True
    print(ord.comfirmed)
    ord.final_price=bets[0].bet_price
    ord.save()
