from django.contrib import admin
from .models import items,item_info,order_path_info,order_bets,order
# Register your models here.
admin.site.register(items)
admin.site.register(item_info)
admin.site.register(order_path_info)
admin.site.register(order_bets)
admin.site.register(order)