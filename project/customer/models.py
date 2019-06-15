from django.db import models

# Create your models here.
"""
should there be a foreign key connecting items and item_info?

order_path_info,order_bets,and order should also have foreign keys?

can we add photos(customer can upload photos about the item) to the item_info  **(not neccessary)

"""

class items(models.Model):
    item_name = models.CharField(max_length=100)
    
class item_info(models.Model):
    order_id = models.CharField(max_length=20)
    item_weight=models.DecimalField(max_digits=20,decimal_places=2)
    item_length=models.DecimalField(max_digits=20,decimal_places=2)
    item_width=models.DecimalField(max_digits=20,decimal_places=2)
    item_height=models.DecimalField(max_digits=20,decimal_places=2)
    handle_with_care = models.BooleanField(default=False)
    item_material=models.CharField(max_length=100)
    item_approximate_cost=models.IntegerField(blank=True,null=True)

class order_path_info(models.Model):
        order_id = models.CharField(max_length=20)
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
        order_id = models.CharField(max_length=20)
        merchant_id=models.CharField(max_length=20)
        bet_price=models.IntegerField()
        extra_info = models.TextField()
        pickup_days=models.IntegerField()

class order(models.Model):
    order_id = models.CharField(max_length=20)
    customer_id = models.CharField(max_length=20)
    merchant_id=models.CharField(max_length=20)
    comfirmed = models.BooleanField(default=False)