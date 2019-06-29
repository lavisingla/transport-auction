from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_verify(models.Manager):
    def check_user(self,username):
        return self.filter(user__username=username)

    def get_merchant_details(self,merchant_id):
        return self.filter(user__username=merchant_id,merchant=True)

    def get_user_details(self,user_id):
        return self.filter(user__username=user_id)



class user_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact=models.IntegerField()
    area=models.CharField(max_length=50)
    city=models.CharField(max_length=30)
    pin_code=models.IntegerField()
    objects=user_verify()
    state=models.CharField(max_length=20)
    orders_completed=models.PositiveIntegerField(default=0)
    ratings=models.PositiveIntegerField(default=0)
    merchant=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
