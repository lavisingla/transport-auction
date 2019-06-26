from django.contrib import admin
from .models import item_info,items,order,order_bets,order_path_info
# Register your models here.
admin.site.register(items)
admin.site.register(item_info)
admin.site.register(order)
admin.site.register(order_bets)
admin.site.register(order_path_info)
