from django.db import models

# Create your models here.

class OrderManager(models.Manager):
    def get_orders_ongoing(self,customer_id):
        return self.filter(customer_id=customer_id,comfirmed=True,completed=False)

    def get_previous_orders(self,customer_id):
        return self.filter(customer_id=customer_id,completed=True,comfirmed= True)

    def get_pending_requests(self,customer_id):
        return self.filter(customer_id=customer_id,comfirmed=False)

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
    completed=models.BooleanField(default=False)
    objects = OrderManager()
