from django.contrib import admin
from .models import item_info,order_path_info,order_bets,order,images_by_customer
# Register your models here.
admin.site.register(order)
admin.site.register(item_info)
admin.site.register(order_path_info)
admin.site.register(order_bets)

admin.site.register(images_by_customer)