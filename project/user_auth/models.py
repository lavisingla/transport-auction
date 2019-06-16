from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_verify(models.Manager):
    def check_user(self,username):
        return self.filter(user__username=username)
        
class user_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact=models.IntegerField()
    area=models.CharField(max_length=50)
    city=models.CharField(max_length=30)
    pin_code=models.IntegerField()
    objects=user_verify()
    state=models.CharField(max_length=20)
    merchantOrUser=models.BooleanField(default=False) # 0 - for User, 1 - for merchant 

    def __str__(self):
        return self.user.username
