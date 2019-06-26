from django.db import models

# Create your models here.

class OrderManager(models.Manager):
    def get_orders_ongoing(self,customer_id):
        return self.filter(customer_id=customer_id,comfirmed=True,completed=False)

    def get_previous_orders(self,customer_id):
        return self.filter(customer_id=customer_id,completed=True,comfirmed= True)

    def get_pending_requests(self,customer_id):
        return self.filter(customer_id=customer_id,comfirmed=False)

class OrderPathInfoManager(models.Manager):
    def get_order_path_info(self,order_id):
        return self.filter(order_id=order_id)

class ItemInfoManager(models.Manager):
    def get_item_info(self,order_id):
        return self.filter(order_id=order_id)

class OrderBetsManager(models.Manager):
    def get_bets(self,order_id):
        return self.filter(order_id=order_id).order_by('bet_price')

class items(models.Model):
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name

class item_info(models.Model):
    order_id = models.CharField(max_length=20)
    objects=ItemInfoManager()
    item_weight=models.DecimalField(max_digits=20,decimal_places=2)
    item_length=models.DecimalField(max_digits=20,decimal_places=2)
    item_width=models.DecimalField(max_digits=20,decimal_places=2)
    item_height=models.DecimalField(max_digits=20,decimal_places=2)
    item_id=models.PositiveIntegerField(null=True)
    handle_with_care = models.BooleanField(default=False)
    item_material=models.CharField(max_length=100)
    auction_life = models.PositiveIntegerField(default=2)
    item_approximate_cost=models.IntegerField(blank=True,null=True)

class order_path_info(models.Model):
        order_id = models.CharField(max_length=20)
        objects=OrderPathInfoManager()
        source_area = models.CharField(max_length=100)
        source_city=models.CharField(max_length=30)
        source_state=models.CharField(max_length=30)
        source_pin=models.IntegerField()
        destination_area = models.CharField(max_length=100)
        destination_city=models.CharField(max_length=30)
        destination_state=models.CharField(max_length=30)
        destination_pin=models.IntegerField()
        expecting_arrival=models.DateField(auto_now=True)

class order_bets(models.Model):
        order_id = models.CharField(max_length=20)
        merchant_id=models.CharField(max_length=20)
        bet_price=models.IntegerField()
        objects=OrderBetsManager()
        extra_info = models.TextField()
        date_of_bet=models.DateField(null=True)
        pickup_days=models.IntegerField()

class order(models.Model):
    order_id = models.CharField(max_length=20)
    timeToLive =models.PositiveIntegerField(default=30)
    item_id=models.PositiveIntegerField(null=True)
    customer_id = models.CharField(max_length=20)
    merchant_id=models.CharField(max_length=20,null=True)
    comfirmed = models.BooleanField(default=False)
    completed=models.BooleanField(default=False)
    final_price=models.IntegerField(default=0)
    date=models.DateField(null=True)
    objects = OrderManager()
