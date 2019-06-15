from django.db import models
from user_auth.models import user_info
# Create your models here.
"""
should there be a foreign key connecting items and item_info?

order_path_info,order_bets,and order should also have foreign keys?

can we add photos(customer can upload photos about the item) to the item_info  **(not neccessary)

"""
class item_info(models.Model):
    item_name = models.CharField(max_length=100)    
    
    item_weight=models.DecimalField(max_digits=20,decimal_places=2)
    item_length=models.DecimalField(max_digits=20,decimal_places=2)
    item_width=models.DecimalField(max_digits=20,decimal_places=2)
    item_height=models.DecimalField(max_digits=20,decimal_places=2)
    handle_with_care = models.BooleanField(default=False)
    item_material=models.CharField(max_length=100)
    item_approximate_cost=models.IntegerField(blank=True,null=True)

    
class order(models.Model):
    item_id = models.ForeignKey(item_info,on_delete=models.CASCADE)    
    customer = models.OneToOneField(user_info,on_delete=models.CASCADE,related_name= 'customer')   
    merchant = models.OneToOneField(user_info,on_delete=models.CASCADE,related_name = 'merchant' )
    comfirmed = models.BooleanField(default=False)

class order_path_info(models.Model):
        order_id  = models.OneToOneField(order,on_delete=models.CASCADE)
        source_area = models.TextField()
        source_city=models.CharField(max_length=30)
        source_state=models.CharField(max_length=30)
        source_pin=models.IntegerField()
        destination_area = models.TextField()
        destination_city=models.CharField(max_length=30)
        destination_state=models.CharField(max_length=30)
        destination_pin=models.IntegerField()
        expecting_arrival=models.DateField(auto_now=True)

class order_bets(models.Model):
        order_id = models.OneToOneField(order,on_delete=models.CASCADE)
        #order_id = models.CharField(max_length=20)
        merchant_id=models.CharField(max_length=20)
        bet_price=models.IntegerField()
        extra_info = models.TextField()
        pickup_days=models.IntegerField()

class images_by_customer(models.Model):
    item_information = models.ForeignKey(item_info,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'item_image/', blank=True)